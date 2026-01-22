# ------------------------------------------------------------------------------
#
#   Copyright 2022 Valory AG
#   Copyright 2018-2021 Fetch.AI Limited
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#
# ------------------------------------------------------------------------------

"""This module contains the handler for the 'metrics' skill."""

import json
import datetime
from typing import cast, get_type_hints

from aea.skills.base import Handler
from aea.protocols.base import Message

from packages.eightballer.protocols.default import DefaultMessage
from packages.eightballer.protocols.http.message import HttpMessage
from packages.eightballer.skills.trading_state.dialogues import (
    HttpDialogue,
    HttpDialogues,
    DefaultDialogues,
)
from packages.eightballer.skills.simple_fsm.strategy import ArbitrageStrategyParams, TZ


class HttpHandler(Handler):
    """This implements the echo handler."""

    SUPPORTED_PROTOCOL = HttpMessage.protocol_id

    def setup(self) -> None:
        """Implement the setup."""

    def handle(self, message: Message) -> None:
        """Implement the reaction to an envelope."""
        http_msg = cast(HttpMessage, message)

        # recover dialogue
        http_dialogues = cast(HttpDialogues, self.context.http_dialogues)
        http_dialogue = cast(HttpDialogue, http_dialogues.update(http_msg))
        if http_dialogue is None:
            self._handle_unidentified_dialogue(http_msg)
            return

        # handle message
        if http_msg.performative == HttpMessage.Performative.REQUEST:
            self._handle_request(http_msg, http_dialogue)
        else:
            self._handle_invalid(http_msg, http_dialogue)

    def _handle_unidentified_dialogue(self, http_msg: HttpMessage) -> None:
        """Handle an unidentified dialogue."""
        self.context.logger.info(f"received invalid http message={http_msg}, unidentified dialogue.")
        default_dialogues = cast(DefaultDialogues, self.context.default_dialogues)
        default_msg, _ = default_dialogues.create(
            counterparty=http_msg.sender,
            performative=DefaultMessage.Performative.ERROR,
            error_code=DefaultMessage.ErrorCode.INVALID_DIALOGUE,
            error_msg="Invalid dialogue.",
            error_data={"http_message": http_msg.encode()},
        )
        self.context.outbox.put_message(message=default_msg)

    def _handle_request(self, http_msg: HttpMessage, http_dialogue: HttpDialogue) -> None:
        """Handle a Http request."""
        self.context.logger.debug(
            f"received http request with method={http_msg.method}, url={http_msg.url} and body={http_msg.body}"
        )
        if http_msg.method == "get" and http_msg.url.find("/metrics"):
            self._handle_get(http_msg, http_dialogue)
        # While we ideally should hit a differently named endpoint here,
        # or, alternatively, use a more structured conversational protocol beyond the generic HTTP
        # For now we use this metrics endpoint to update the agent trading strategy state
        elif http_msg.method == "post" and http_msg.url.find("/metrics"):
            self._handle_post(http_msg, http_dialogue)
        else:
            self._handle_invalid(http_msg, http_dialogue)

    def _handle_get(self, http_msg: HttpMessage, http_dialogue: HttpDialogue) -> None:
        """Handle a Http request of verb GET."""
        if self.enable_cors:
            cors_headers = "Access-Control-Allow-Origin: *\n"
            cors_headers += "Access-Control-Allow-Methods: POST\n"
            cors_headers += "Access-Control-Allow-Headers: Content-Type,Accept\n"
            headers = cors_headers + http_msg.headers
        else:
            headers = http_msg.headers

        # we ensure that it is application/jsonS
        if not headers.startswith("Content-Type: application/json"):
            headers = "Content-Type: application/json\n" + headers
        # we ensure that it is application/jsonS

        response = self.context.shared_state.get("state")
        data = response.to_json().encode("utf-8") if response else b"{}"

        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=200,
            status_text="Success",
            headers=headers,
            body=data,
        )
        self.context.logger.debug(f"responding with: {http_response}")
        self.context.outbox.put_message(message=http_response)

    def _handle_post(self, http_msg: HttpMessage, http_dialogue: HttpDialogue) -> None:
        """Handle a Http request of verb POST."""

        # We dump the incoming POST request to update the trading strategy parameters in the shared state,
        # which we will subsquently pick up in the CoolDownRound to update the trading strategy state,
        # as to not  cause a conflict by updating this state mid-flight during trade execution.

        received_params = json.loads(http_msg.body)
        agent_state = self.context.shared_state.get("state")
        type_hints = get_type_hints(ArbitrageStrategyParams)
        typed_params = {}
        for key, value in received_params.items():
            if (expected_type := type_hints.get(key)) is None:
                self.context.logger.warning(f"Unexpected arbitrage strategy parameter: {key}: ignoring")
                continue
            try:
                typed_value = expected_type(value)
            except Exception:
                msg = f"Failed to cast arbitrage strategy parameter {key} value {value} to {expected_type}: ignoring"
                self.context.logger.warning(msg)
                continue
            typed_params[key] = typed_value

        agent_state.arbitrage_strategy_params_update_request = typed_params

        response_payload = {
            "status": "accepted",
            "message": "Parameters recorded and scheduled for application during CoolDownRound.",
            "applied": False,
            "received_at": datetime.datetime.now(tz=TZ).isoformat(),
            "params": typed_params,
        }
        body = json.dumps(response_payload).encode("utf-8")

        http_response = http_dialogue.reply(
            performative=HttpMessage.Performative.RESPONSE,
            target_message=http_msg,
            version=http_msg.version,
            status_code=200,
            status_text="Success",
            headers=http_msg.headers,
            body=body,
        )

        self.context.logger.info(f"responding with: {http_response}")
        self.context.outbox.put_message(message=http_response)

    def _handle_invalid(self, http_msg: HttpMessage, http_dialogue: HttpDialogue) -> None:
        """Handle an invalid http message."""
        self.context.logger.warning(
            f"""
            Cannot handle http message of
            performative={http_msg.performative}
            dialogue={http_dialogue.dialogue_label}.
            """
        )

    def teardown(self) -> None:
        """Implement the handler teardown."""

    def __init__(self, **kwargs):
        """Initialise the handler."""
        self.enable_cors = kwargs.pop("enable_cors", True)
        super().__init__(**kwargs)
