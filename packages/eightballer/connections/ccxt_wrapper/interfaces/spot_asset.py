"""Interface for the Spot asset."""

import asyncio

from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage
from packages.eightballer.protocols.spot_asset.dialogues import SpotAssetDialogue, BaseSpotAssetDialogues
from packages.eightballer.protocols.spot_asset.custom_types import Decimal
from packages.eightballer.connections.ccxt_wrapper.interfaces.interface_base import BaseInterface


INTERVAL = 10
DEFAULT_SPOT_ASSET = {
    "total": 0.0,
    "free": 0.0,
    "availableWithoutBorrow": 0.0,
}
DERIBIT_ASSETS = ["ETH", "BTC", "USDC", "SOL"]


class SpotAssetInterface(BaseInterface):
    """Spot asset interface."""

    protocol_id = SpotAssetMessage.protocol_id
    dialogue_class = SpotAssetDialogue
    dialogues_class = BaseSpotAssetDialogues
    _balances = {}
    started = False

    async def get_spot_asset(self, message, dialogue, connection):
        """Handle get_spot_asset."""
        connection.logger.debug("Received request to poll balances : %s", message.name)
        if not self.started:
            connection.loop.create_task(self._poll_balances(message, connection))

        asset_balances = await self._get_balances(message, connection)
        total = Decimal(asset_balances["total"])
        free = Decimal(asset_balances["free"])
        avail = Decimal(asset_balances["availableWithoutBorrow"])
        response = dialogue.reply(
            performative=SpotAssetMessage.Performative.SPOT_ASSET,
            name=message.name,
            total=total,
            free=free,
            available_without_borrow=avail,
        )
        connection.logger.debug(f"Returning from order interface : {response}")
        return response

    def _parse_result_ftx(self, res, message):
        self._balances[message.exchange_id] = {k["coin"]: k for k in res["info"]["result"]}

    def _parse_result_other(self, res, message):
        self._balances[message.exchange_id] = {k["asset"]: k for k in res["info"]["balances"]}
        asset = self._balances[message.exchange_id][message.name]
        asset["total"] = float(asset["free"]) + float(asset["locked"])
        asset["availableWithoutBorrow"] = asset["free"]

    async def _get_balances(self, message, connection):
        try:
            exchange = connection.exchanges.get(message.exchange_id, None)
            if message.exchange_id == "deribit":
                res = []
                for asset in DERIBIT_ASSETS:
                    balance = await exchange.fetch_balance({"currency": asset})
                    balance["asset"] = asset
                    balance["total"] = balance["total"][asset]
                    balance["free"] = balance["free"][asset]
                    balance["locked"] = balance["total"] - balance["free"]
                    res.append(balance)
                res = {"info": {"balances": res}}
            else:
                res = await exchange.fetch_balance(message.name)
            connection.logger.debug("Updated balances: %s", message.exchange_id)
            if exchange is None:
                msg = "Unsupported exchange {message.exchange_id}"
                raise ValueError(msg)
            self._parse_result_other(res, message)
            return self._balances[message.exchange_id][message.name]
        except Exception as error:  # pylint: disable=W0703
            connection.logger.exception(f"FAILED TO POLL WITH -> {error}!")

    async def _poll_balances(self, message, connection):
        connection.logger.info("Starting to poll balances : %s", message.name)
        self.started = True
        self._balances[message.exchange_id] = {}
        while True:
            await self._get_balances(message, connection)
            await asyncio.sleep(INTERVAL)
