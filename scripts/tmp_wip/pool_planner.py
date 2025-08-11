import requests
import numpy as np
import pandas as pd
from functools import reduce
from scipy.optimize import minimize
from rich.logging import RichHandler

def optimize_balancer_portfolio(
    assets_data,               # Dictionary with asset data
    balancer_api_data,         # API data from Balancer
    core_allocations,          # Core allocations like OLAS:50%, wBTC:5%, lBTC:5%
    min_allocations=None,      # Minimum allocations for specific assets
    max_allocations=None,      # Maximum allocations for specific assets
    risk_free_rate=0.01,       # Risk-free rate for Sharpe calculation
    volume_weight=0.4,         # Weight for volume-based optimization
    sharpe_weight=0.6,         # Weight for Sharpe ratio optimization
    correlation_matrix=None    # Correlation matrix between assets
):
    """
    Optimize a Balancer pool portfolio based on risk-adjusted returns and volume capture.
    
    Parameters:
    -----------
    assets_data : dict
        Dictionary containing asset data with keys:
        - 'returns': Expected returns for each asset
        - 'volatility': Volatility (standard deviation) for each asset
        - 'is_staking_derivative': Boolean indicating if asset is a staking derivative
    balancer_api_data : dict
        Data from Balancer API about pool volumes and liquidity
    core_allocations : dict
        Core allocation requirements (e.g., {'OLAS': 0.5, 'wBTC': 0.05, 'lBTC': 0.05})
    min_allocations : dict, optional
        Minimum allocation for each asset
    max_allocations : dict, optional
        Maximum allocation for each asset
    risk_free_rate : float, optional
        Risk-free rate for Sharpe ratio calculation
    volume_weight : float, optional
        Weight given to volume-based optimization
    sharpe_weight : float, optional
        Weight given to Sharpe ratio optimization
    correlation_matrix : pd.DataFrame, optional
        Correlation matrix between assets
    
    Returns:
    --------
    dict
        Optimized portfolio allocations
    """
    # Extract assets from data
    all_assets = list(assets_data.keys())
    non_core_assets = [asset for asset in all_assets if asset not in core_allocations]
    
    # Calculate volume-to-liquidity ratio for each asset
    volume_liquidity_ratios = {}
    for asset in all_assets:
        volume_liquidity_ratios[asset] = calculate_volume_liquidity_ratio(asset, balancer_api_data)
    
    # Normalize volume-liquidity ratios
    total_ratio = sum(volume_liquidity_ratios.values())
    normalized_ratios = {asset: ratio/total_ratio for asset, ratio in volume_liquidity_ratios.items()}
    
    # Calculate remaining allocation after core assets
    remaining_allocation = 1.0 - sum(core_allocations.values())
    
    def objective(weights):
        # Convert weights list to dictionary for non-core assets
        non_core_weights = dict(zip(non_core_assets, weights))

        # Combine with core allocations
        all_weights = {**core_allocations, **non_core_weights}

        # Check data types before calculations
        for asset in all_assets:
            if not isinstance(assets_data[asset]['returns'], (int, float)):
                print(f"Warning: Returns for {asset} is not a scalar: {type(assets_data[asset]['returns'])}")
                assets_data[asset]['returns'] = float(assets_data[asset]['returns'])
            if not isinstance(assets_data[asset]['volatility'], (int, float)):
                print(f"Warning: Volatility for {asset} is not a scalar: {type(assets_data[asset]['volatility'])}")
                assets_data[asset]['volatility'] = float(assets_data[asset]['volatility'])

        # Calculate expected return
        expected_return = 0
        for asset in all_assets:
            contribution = all_weights[asset] * assets_data[asset]['returns']
            expected_return += contribution

        # Calculate portfolio volatility
        portfolio_variance = 0
        if correlation_matrix is not None:
            portfolio_volatility = calculate_portfolio_volatility(all_weights, assets_data, correlation_matrix)
        else:
            for asset in all_assets:
                contribution = all_weights[asset]**2 * assets_data[asset]['volatility']**2
                portfolio_variance += contribution
            portfolio_volatility = np.sqrt(portfolio_variance)

        # Calculate Sharpe ratio
        sharpe_ratio = (expected_return - risk_free_rate) / max(portfolio_volatility, 1e-10)

        # Calculate volume capture score
        volume_capture = 0
        for asset in all_assets:
            contribution = all_weights[asset] * normalized_ratios[asset]
            volume_capture += contribution

        # Combined objective (negative because we're minimizing)
        result = -(sharpe_weight * sharpe_ratio + volume_weight * volume_capture)

        # Ensure we have a scalar
        if not isinstance(result, (int, float)):
            print(f"Warning: Result is not a scalar: {type(result)}, value: {result}")

        return float(result)

    
    # Initial guess for non-core assets (equal distribution)
    initial_weights = [remaining_allocation / len(non_core_assets)] * len(non_core_assets)
    
    # Constraints
    constraints = [
        {'type': 'eq', 'fun': lambda w: sum(w) - remaining_allocation}  # Sum of non-core weights equals remaining allocation
    ]
    
    # Bounds for non-core assets
    bounds = []
    for asset in non_core_assets:
        min_val = min_allocations.get(asset, 0.0) if min_allocations else 0.0
        max_val = max_allocations.get(asset, 1.0) if max_allocations else 1.0
        bounds.append((min_val, max_val))
    
    # Optimize
    result = minimize(objective, initial_weights, method='SLSQP', bounds=bounds, constraints=constraints)
    
    # Combine core and optimized non-core allocations
    optimized_weights = {**core_allocations}
    for i, asset in enumerate(non_core_assets):
        optimized_weights[asset] = result.x[i]
    
    return optimized_weights

def calculate_volume_liquidity_ratio(asset, balancer_api_data):
    """
    Calculate volume-to-liquidity ratio for an asset based on Balancer API data.
    
    Parameters:
    -----------
    asset : str
        Asset symbol
    balancer_api_data : dict
        Data from Balancer API
    
    Returns:
    --------
    float
        Volume-to-liquidity ratio
    """
    total_volume = 0
    total_liquidity = 0
    
    # Sum up volume and liquidity for all pools containing this asset
    for pool in balancer_api_data['pools']:
        if asset in pool['assets']:
            # Get the asset's share of pool volume based on its weight
            asset_weight = pool['weights'][asset]
            pool_volume = pool['volume_24h']
            pool_liquidity = pool['liquidity']
            
            asset_volume = pool_volume * asset_weight
            asset_liquidity = pool_liquidity * asset_weight
            
            total_volume += asset_volume
            total_liquidity += asset_liquidity
    
    # Avoid division by zero
    if total_liquidity == 0:
        return 0
    
    return total_volume / total_liquidity

def calculate_portfolio_volatility(weights, assets_data, correlation_matrix):
    """
    Calculate portfolio volatility using correlation matrix.
    
    Parameters:
    -----------
    weights : dict
        Asset weights
    assets_data : dict
        Asset data including volatility
    correlation_matrix : pd.DataFrame
        Correlation matrix between assets
    
    Returns:
    --------
    float
        Portfolio volatility
    """
    volatility = 0.0
    assets = list(weights.keys())
    
    for i, asset_i in enumerate(assets):
        for j, asset_j in enumerate(assets):
            volatility += weights[asset_i] * weights[asset_j] * \
                         assets_data[asset_i]['volatility'] * \
                         assets_data[asset_j]['volatility'] * \
                         correlation_matrix.loc[asset_i, asset_j]
    
    return volatility ** 0.5


def process_staking_derivatives(assets_data):
    """
    Process staking derivatives to include APY premium in returns.
    """
    for asset, data in assets_data.items():
        if data['is_staking_derivative']:
            # Add staking yield to expected returns
            data['returns'] += data['staking_apy']
    return assets_data

# Core allocations as per your requirements
core_allocations = {
    'OLAS': 0.5,
    'WBTC': 0.05,
    'LBTC': 0.05
}

# Min allocations to ensure we have some stables and staking derivatives
min_allocations = {
    'USDC': 0.01,
    'WETH': 0.01,
    'WSTETH': 0.01,
    'RETH': 0.01,
    'SUSDS': 0.01,
    'SUSDE': 0.01,
    'CBETH': 0.01,
    'STETH': 0.01,
}
yield_bearing_assets = [
    'STETH', 
    'WSTETH', 
    'RETH', 
    'CBETH', 
    "SUSDS", 
    "SUSDE"
]

def get_defi_yields():
    """
    Get yield data from DeFiLlama API for major staking derivatives
    
    Returns:
    --------
    dict
        Dictionary with APY data for staking derivatives
    """
        # DeFiLlama pools API
    response = requests.get('https://yields.llama.fi/pools')
    data = response.json()
        
    whitelisted_projects = [
        "lido",
        "rocket-pool",
        "aave-v3",
        "compound",
        "makerdao",
        "spark",
        "coinbase-wrapped-staked-eth",
        "ether.fi-stake",
        "ethena-usde"

    ]
    # Extract APYs for relevant tokens
    apys = {}
    mainnet_key = "Ethereum"
    project_data = filter(lambda x: x.get('project') in whitelisted_projects, data['data'])
    chain_data = filter(lambda x: x.get('chain') == mainnet_key , project_data)
    pool_data = filter(lambda x: x.get('symbol') in yield_bearing_assets, chain_data)

    # we use reduce to collect the max apy for each asset
    def collect_apys(pool_data):
        apys = {}
        for pool in pool_data:
            asset = pool['symbol']
            apy = pool['apy']
            if asset not in apys:
                apys[asset] = apy
            else:
                apys[asset] = max(apys[asset], apy)
        return apys
    apys = collect_apys(pool_data)
    return apys
    
# Get staking derivative yields


def get_asset_data():
    """
    Fetch asset data from various sources.
    Returns dictionary with asset data.
    """
    # Implementation would fetch data from various sources
    yields = get_defi_yields()

    def get_returns_over_time(asset):
        # Implementation would fetch historical returns for the asset
        return np.random.normal(0., 0.1)
    
    def get_volatility_over_time(asset):
        # Implementation would fetch historical volatility for the asset
        return np.random.normal(0., 0.1)
    
    # Combine data from different sources
    asset_data = {}
    for asset in yields:
        asset_data[asset] = {
            'returns': get_returns_over_time(asset),
            'volatility': get_volatility_over_time(asset),
            'is_staking_derivative': True,
            'staking_apy': yields[asset]
        }

    # we now get the data for the non-staking derivatives
    non_staking_derivative_assets = [
        'OLAS',
        'WBTC',
        'USDC',
        'DAI',
        'WETH',
        'LBTC',
        'RETH',
        ]
    
    for asset in non_staking_derivative_assets:
        asset_data[asset] = {
            'returns': get_returns_over_time(asset),
            'volatility': get_volatility_over_time(asset),
            'is_staking_derivative': False,
            'staking_apy': 0.0
        }

    return asset_data

def get_balancer_api_data():
    """
    Fetch data from Balancer API.
    Returns dictionary with pool data.
    """
    return {
        'pools': [
            {
                'assets': ['OLAS', 'wBTC'],
                'weights': {'OLAS': 0.6, 'wBTC': 0.4},
                'volume_24h': 1000000,
                'liquidity': 500000
            },
            {
                'assets': ['OLAS', 'lBTC'],
                'weights': {'OLAS': 0.7, 'lBTC': 0.3},
                'volume_24h': 500000,
                'liquidity': 300000
            }
        ]
    }
# Get asset data and Balancer API data
assets_data = get_asset_data()  # You'll need to implement this
balancer_api_data = get_balancer_api_data()

# Include staking yields in returns
assets_data = process_staking_derivatives(assets_data)

# Run optimization
optimized_portfolio = optimize_balancer_portfolio(
    assets_data=assets_data,
    balancer_api_data=balancer_api_data,
    core_allocations=core_allocations,
    min_allocations=min_allocations,
    volume_weight=0.4,
    sharpe_weight=0.6
)

print("Optimized Portfolio Weights:")
for asset, weight in optimized_portfolio.items():
    print(f"{asset}: {weight:.2%}")

# Core allocations as per your requirements
core_allocations = {
    'OLAS': 0.5,
}

# Min allocations to ensure we have some stables and staking derivatives
min_allocations = {
    'WBTC': 0.05,
    'lBTC': 0.05,
    'USDC': 0.05,
    'DAI': 0.01,
    'WETH': 0.01,
    'WSTETH': 0.01,
    'RETH': 0.01,
}

# Get asset data and Balancer API data
assets_data = get_asset_data()  # You'll need to implement this
balancer_api_data = get_balancer_api_data()

# Include staking yields in returns
assets_data = process_staking_derivatives(assets_data)

# Run optimization
optimized_portfolio = optimize_balancer_portfolio(
    assets_data=assets_data,
    balancer_api_data=balancer_api_data,
    core_allocations=core_allocations,
    min_allocations=min_allocations,
    volume_weight=0.4,
    sharpe_weight=0.6
)

print("Optimized Portfolio Weights:")
for asset, weight in optimized_portfolio.items():
    print(f"{asset}: {weight:.2%}")