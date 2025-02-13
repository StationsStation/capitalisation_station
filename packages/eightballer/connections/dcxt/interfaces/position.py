"""Interface for the positios protocol."""

from packages.eightballer.connections.dcxt import dcxt
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue, BasePositionsDialogues
from packages.eightballer.protocols.positions.custom_types import Position, Positions
from packages.eightballer.connections.dcxt.interfaces.interface_base import BaseInterface


def all_positions_from_api_call(api_call):
    """Get all positions from the exchange."""
    positions = []
    for position in api_call:
        if "size" in position.get("info", {}):
            position["size"] = float(position["info"]["size"])
        positions.append(Position.from_api_call(position))
    return Positions(positions=positions)


class PositionInterface(BaseInterface):
    """Interface for positions protocol."""

    protocol_id = PositionsMessage.protocol_id
    dialogue_class = PositionsDialogue
    dialogues_class = BasePositionsDialogues

    async def get_all_positions(
        self, message: PositionsMessage, dialogue: PositionsDialogue, connection
    ) -> PositionsMessage | None:
        """Get all positions from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        try:
            params = {}
            for key, value in message.params.items():
                params[key] = value.decode()
            positions = await exchange.fetch_positions(params=params)
            positions = all_positions_from_api_call(positions)
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.ALL_POSITIONS,
                target_message=message,
                positions=positions,
                exchange_id=message.exchange_id,
            )
        except dcxt.exceptions.RequestTimeout:
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.ERROR,
                target_message=message,
                error_code=PositionsMessage.ErrorCode.API_ERROR,
                error_msg="Request timeout",
            )
        except dcxt.exceptions.AuthenticationError:
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.ERROR,
                target_message=message,
                error_code=PositionsMessage.ErrorCode.API_ERROR,
                error_msg="Authentication error",
            )

        except Exception as error:
            connection.logger.exception(f"Error: {error}")
            raise

        return response_message

    async def get_position(
        self, message: PositionsMessage, dialogue: PositionsDialogue, connection
    ) -> PositionsMessage | None:
        """Get a position from the exchange."""
        exchange = connection.exchanges[message.exchange_id]
        try:
            position = await exchange.fetch_position(
                message.position_id,
            )

            position = Position.from_api_call(position)
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.POSITION,
                target_message=message,
                position=position,
                exchange_id=message.exchange_id,
            )
        except dcxt.exceptions.RequestTimeout:
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.ERROR,
                target_message=message,
                error_code=PositionsMessage.ErrorCode.API_ERROR,
                error_msg="Request timeout",
            )
        except dcxt.exceptions.BadSymbol:
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.ERROR,
                target_message=message,
                error_code=PositionsMessage.ErrorCode.UNKNOWN_POSITION,
                error_msg=message.position_id,
            )
        except dcxt.exceptions.AuthenticationError:
            response_message = dialogue.reply(
                performative=PositionsMessage.Performative.ERROR,
                target_message=message,
                error_code=PositionsMessage.ErrorCode.API_ERROR,
                error_msg="Authentication error",
            )
        return response_message
