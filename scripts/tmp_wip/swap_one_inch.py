# How to Use the 1inch Swap API in Python
# Step 1: Install the required packages
# 
# 💡 If you have python ≥v3 installed you can use pip3 otherwise you can use pip install
# pip3 install requests web3
# Step 2: Set up your environment
# 
# Replace “[YOUR_API_KEY]” with the API key found here.
# 
# import requests
# from web3 import Web3
# 
# chainId = 56  # Chain ID for Binance Smart Chain (BSC)
# web3RpcUrl = "https://bsc-dataseed.binance.org"  # URL for BSC node
# headers = { "Authorization": "Bearer [YOUR_API_KEY]", "accept": "application/json" }
# walletAddress = "0x...xxx"  # Your wallet address
# privateKey = "0x...xxx"  # Your wallet's private key. NEVER SHARE THIS WITH ANYONE!
# Step 3: Define your swap parameters
# 
# swapParams = {
#     "src": "0x111111111117dc0aa78b770fa6a738034120c302",  # Token address of 1INCH
#     "dst": "0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3",  # Token address of DAI
#     "amount": "100000000000000000",  # Amount of 1INCH to swap (in wei)
#     "from": walletAddress,
#     "slippage": 1,  # Maximum acceptable slippage percentage for the swap (e.g., 1 for 1%)
#     "disableEstimate": False,  # Set to True to disable estimation of swap details
#     "allowPartialFill": False,  # Set to True to allow partial filling of the swap order
# }
# Step 4: Define API URLs and initialize Web3 libraries (Optional if not using Web3)
# 
# apiBaseUrl = f"https://api.1inch.dev/swap/v6.0/{chainId}"
# web3 = Web3(web3RpcUrl);
# Step 5: Define Helper Functions
# 
# # Construct full API request URL
# def apiRequestUrl(methodName, queryParams):
#     return f"{apiBaseUrl}{methodName}?{'&'.join([f'{key}={value}' for key, value in queryParams.items()])}

# def buildTxForSwap(swapParams):
#     url = apiRequestUrl("/swap", swapParams)
#     swapTransaction = requests.get(url,  headers={'Authorization': f'Bearer YOUR_API_KEY'}).json()["tx"]
#     return swapTransaction
# we convert this to a nice class as so

import os
from pathlib import Path
import sys
import requests
from aea_ledger_ethereum import EthereumApi, EthereumCrypto
from dataclasses import dataclass
import rich_click as click
from rich import print
from web3 import Web3
from deposit_to_drv import check_allowance, check_balance, increase_allowance, load_contract
from packages.eightballer.contracts.erc_20.contract import Erc20
from packages.eightballer.connections.dcxt.dcxt.one_inch import OneInchSwapApi, SPENDER, OneInchSwapParams, InsufficientAllowance, InsufficientBalance



print(Web3.to_checksum_address(SPENDER["1"]))
print(SPENDER["1"])

    
@click.command()
@click.option(
    '--chain_id', 
    type=int, 
    help='Chain ID for chain to swap on',
    default=1
)
@click.option(
    '--api_key', 
    type=str, 
    help='API key for 1inch API',
    default=None
)
@click.option(
    '--src', 
    type=str, 
    help='Source token address: (usdc)',
    default="0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48"
)
@click.option(
    '--dst', 
    type=str, 
    help='Destination token address: (lbtc)',
    default="0x8236a87084f8b84306f72007f36f2618a5634494"
)
@click.option(
    '--amount', 
    type=int, 
    help='Amount of tokens to swap',
    default="10000000"
)
def main(
    chain_id, 
    api_key,
    src,
    dst,
    amount
    ):
    """
    Swap tokens using the 1inch API.

    Args:
        chain_id (int): Chain ID for chain to swap on.
        api_key (str): API key for 1inch API.
    """

    api = EthereumApi(
        address="https://eth.drpc.org",
        chain_id=str(chain_id),
    )
    crypto = EthereumCrypto(
        private_key_path="ethereum_private_key.txt",
    )

    print(f"Using chain ID:     {chain_id}")
    print(f"Crypto Address:     {crypto.address}")

    swap_params = OneInchSwapParams(
        src=src,
        dst=dst,
        amount=amount,
        from_=crypto.address,
        slippage=1,
        disable_estimate=False,
        allow_partial_fill=False
    )

    erc_20 = load_contract(Path("packages/eightballer/contracts/erc_20"))



    def get_erc_details(contract, api, address):
        decimals = contract.decimals(api, address)['int']
        balance = contract.balance_of(api, address, crypto.address)['int']
        symbol = contract.symbol(api, address)['str']
        return decimals, balance, symbol
    
    def get_allowance(contract, api, owner, spender):
        allowance = contract.allowance(
            api, 
            src,
            owner, 
            spender
            )['int']
        return allowance
    

    spent_erc_20_decimals, spent_erc_20_balance, spent_erc_20_symbol = get_erc_details(erc_20, api, src)
    bought_erc_20_decimals, bought_erc_20_balance, bought_erc_20_symbol = get_erc_details(erc_20, api, dst)

    print("Spent token:", src)
    print(f"    Symbol:     {spent_erc_20_symbol}")
    print(f"    Decimals:   {spent_erc_20_decimals}")
    print(f"    Balance:    {spent_erc_20_balance}")
    print(f"    Human bal:  {spent_erc_20_balance / 10**spent_erc_20_decimals}")

    print("Bought token:", dst)
    print(f"    Symbol:     {bought_erc_20_symbol}")
    print(f"    Decimals:   {bought_erc_20_decimals}")
    print(f"    Balance:    {bought_erc_20_balance}")
    print(f"    Human bal:  {bought_erc_20_balance / 10**bought_erc_20_decimals}")


    if spent_erc_20_balance < amount:
        raise InsufficientBalance("Insufficient balance in source token")
    
    allowance = get_allowance(erc_20, api, crypto.address, SPENDER[str(chain_id)])
    if allowance < amount:
        print("Increasing allowance")
        result = increase_allowance(
            token_address=src,
            spender=SPENDER[str(chain_id)],
            amount=amount,
            ledger_api=api,
            crypto=crypto
        )
        if not result:
            raise InsufficientAllowance("Failed to increase allowance")

    one_inch_api = OneInchSwapApi(
        api, 
        crypto, 
        chain_id, 
        "http://gnosis.chains.etf:8545", 
        api_key=os.environ["ONE_INCH_API_KEY"]
    )
    price_quote = one_inch_api.get_quote(swap_params)
    in_amt_human = amount / 10**spent_erc_20_decimals
    out_amt_human = int(price_quote["dstAmount"]) / 10**bought_erc_20_decimals

    ratio = in_amt_human / out_amt_human
    invert_ratio = 1 / ratio

    print(f"Rates:")
    print(f"    Expected human input amount:        {in_amt_human}")
    print(f"    Expected human output amount:       {out_amt_human}")
    print(f"    Market:                             {bought_erc_20_symbol}/{spent_erc_20_symbol}")
    print(f"    Price ratio:                        {ratio}")
    print(f"    Inverted Market:                    {spent_erc_20_symbol}/{bought_erc_20_symbol}")
    print(f"    Inverted price ratio:               {invert_ratio}")
    print(f"    Price quote:                        {price_quote}")

    if not input("Proceed with swap? (y/n): ").lower() == "y":
        sys.exit(0)
    one_inch_api.swap_tokens(swap_params)


if __name__ == "__main__":
    main()
