"""This module contains the scaffold contract definition."""

# ruff: noqa: PLR0904
from aea.common import JSONLike
from aea.crypto.base import Address, LedgerApi
from aea.contracts.base import Contract
from aea.configurations.base import PublicId


class NablaQuote(Contract):
    """The scaffold contract class for a smart contract."""

    contract_id = PublicId.from_str("open_aea/scaffold:0.1.0")

    @classmethod
    def nabla_portal(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
    ) -> JSONLike:
        """Handler method for the 'nabla_portal' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.nablaPortal().call()
        return {"address": result}

    @classmethod
    def quote(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        token_path: list[Address],
        router_path: list[Address],
        token_prices: list[int],
    ) -> JSONLike:
        """Handler method for the 'quote' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.quote(
            _amountIn=amount_in,
            _tokenPath=token_path,
            _routerPath=router_path,
            _tokenPrices=token_prices,
        ).call()
        return {"bidAmountOut_": result[0], "askAmountOut_": result[1]}

    @classmethod
    def quote_calldata(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        amount_in: int,
        token_path: list[Address],
        router_path: list[Address],
        token_prices: list[int],
    ) -> str:
        """Return calldata for the 'quote' function."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.quote(  # noqa: SLF001
            _amountIn=amount_in,
            _tokenPath=token_path,
            _routerPath=router_path,
            _tokenPrices=token_prices,
        )._encode_transaction_data()

    @classmethod
    def quote_with_reference_price(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        bid_amount_in: int,
        ask_amount_in: int,
        token_path: list[Address],
        router_path: list[Address],
        token_prices: list[int],
    ) -> JSONLike:
        """Handler method for the 'quote_with_reference_price' requests."""
        instance = cls.get_instance(ledger_api, contract_address)
        result = instance.functions.quoteWithReferencePrice(
            _bidAmountIn=bid_amount_in,
            _askAmountIn=ask_amount_in,
            _tokenPath=token_path,
            _routerPath=router_path,
            _tokenPrices=token_prices,
        ).call()
        return {"bidAmountOut_": result[0], "askAmountOut_": result[1]}

    @classmethod
    def quote_with_reference_price_calldata(
        cls,
        ledger_api: LedgerApi,
        contract_address: str,
        bid_amount_in: int,
        ask_amount_in: int,
        token_path: list[Address],
        router_path: list[Address],
        token_prices: list[int],
    ) -> str:
        """Return calldata for the 'quote_with_reference_price' function."""
        instance = cls.get_instance(ledger_api, contract_address)
        return instance.functions.quoteWithReferencePrice(  # noqa: SLF001
            _bidAmountIn=bid_amount_in,
            _askAmountIn=ask_amount_in,
            _tokenPath=token_path,
            _routerPath=router_path,
            _tokenPrices=token_prices,
        )._encode_transaction_data()
