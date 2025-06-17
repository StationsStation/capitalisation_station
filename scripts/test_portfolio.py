"""
We output the portfolio totals.
"""
import requests

from packages.eightballer.protocols.balances.custom_types import Balance


HOST = "http://localhost:8911"

if __name__ == "__main__":
    response = requests.get(f"{HOST}/portfolio")
    if response.status_code != 200:
        raise Exception(f"Failed to fetch portfolio: {response.status_code} {response.text}")

    portfolio_data = response.json().get("portfolio", {})
    print("Portfolio Totals:")
    print("-" * 20)

    currencies_of_interest = [
        "DRV",
        "USDC",
    ]
    for chain, exchanges, in portfolio_data.items():
        print(f"Chain: {chain}")
        for exchange, balances in exchanges.items():
            print(f"  Exchange: {exchange}")
            for balance in balances:
                balance: Balance = Balance(**balance) if isinstance(balance, dict) else balance
                if balance.asset_id not in currencies_of_interest:
                    continue 
                print(f"    - {balance.asset_id}: {balance.free}")