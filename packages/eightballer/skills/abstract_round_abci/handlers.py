# ------------------------------------------------------------------------------
#
#   Copyright 2021-2023 Valory AG
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

"""This module contains the handler for the 'abstract_round_abci' skill."""

import json
import ipaddress
from abc import ABC
from enum import Enum
from typing import Any, cast
from calendar import timegm
from dataclasses import asdict
from collections.abc import Callable

from aea.skills.base import Handler
from aea.protocols.base import Message
from aea.protocols.dialogue.base import Dialogue, Dialogues
from aea.configurations.data_types import PublicId

from packages.valory.protocols.abci import AbciMessage
from packages.valory.protocols.http import HttpMessage
from packages.valory.protocols.ipfs import IpfsMessage
from packages.open_aea.protocols.signing import SigningMessage
from packages.valory.protocols.ledger_api import LedgerApiMessage
from packages.valory.protocols.contract_api import ContractApiMessage
from packages.valory.protocols.abci.custom_types import Events, ValidatorUpdates
from packages.valory.protocols.tendermint.message import TendermintMessage
from packages.valory.skills.abstract_abci.handlers import ABCIHandler
from packages.valory.protocols.tendermint.dialogues import (
    TendermintDialogue,
    TendermintDialogues,
)
from packages.eightballer.skills.abstract_round_abci.base import (
    OK_CODE,
    ERROR_CODE,
    DEFAULT_PENDING_OFFENCE_TTL,
    OffenseType,
    Transaction,
    AddBlockError,
    PendingOffense,
    ABCIAppInternalError,
    SignatureNotValidError,
    LateArrivingTransaction,
    TransactionNotValidError,
    TransactionTypeNotRecognizedError,
)
from packages.eightballer.skills.abstract_round_abci.models import (
    Requests,
    SharedState,
    TendermintRecoveryParams,
)
from packages.eightballer.skills.abstract_round_abci.dialogues import AbciDialogue
from packages.eightballer.skills.abstract_round_abci.behaviours import AbstractRoundBehaviour


def exception_to_info_msg(exception: Exception) -> str:
    """Transform an exception to an info string message."""
    return f"{exception.__class__.__name__}: {exception!s}"


class ABCIRoundHandler(ABCIHandler):
    """ABCI handler."""

    SUPPORTED_PROTOCOL = AbciMessage.protocol_id

    def info(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle the 'info' request.

        As per Tendermint spec (https://github.com/tendermint/spec/blob/038f3e025a19fed9dc96e718b9834ab1b545f136/spec/abci/abci.md#info):

        - Return information about the application state.
        - Used to sync Tendermint with the application during a handshake that happens on startup.
        - The returned app_version will be included in the Header of every block.
        - Tendermint expects last_block_app_hash and last_block_height to be updated during Commit, ensuring that Commit is never called twice for the same block height.

        :param message: the ABCI request.
        :param dialogue: the ABCI dialogue.
        :return: the response.
        """
        # some arbitrary information
        info_data = ""
        # the application software semantic version
        version = ""
        # the application protocol version
        app_version = 0
        # latest block for which the app has called Commit
        last_block_height = self.context.state.round_sequence.height
        # latest result of Commit
        last_block_app_hash = self.context.state.round_sequence.root_hash
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_INFO,
            target_message=message,
            info_data=info_data,
            version=version,
            app_version=app_version,
            last_block_height=last_block_height,
            last_block_app_hash=last_block_app_hash,
        )
        return cast(AbciMessage, reply)

    def init_chain(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle a message of REQUEST_INIT_CHAIN performative.

        As per Tendermint spec (https://github.com/tendermint/spec/blob/038f3e025a19fed9dc96e718b9834ab1b545f136/spec/abci/abci.md#initchain):

        - Called once upon genesis.
        - If ResponseInitChain.Validators is empty, the initial validator set will be the RequestInitChain.Validators.
        - If ResponseInitChain.Validators is not empty, it will be the initial validator set (regardless of what is in RequestInitChain.Validators).
        - This allows the app to decide if it wants to accept the initial validator set proposed by tendermint (ie. in the genesis file), or if it wants to use a different one (perhaps computed based on some application specific information in the genesis file).

        :param message: the ABCI request.
        :param dialogue: the ABCI dialogue.
        :return: the response.
        """
        # Initial validator set (optional).
        validators: list = []
        # Get the root hash of the last round transition as the initial application hash.
        # If no round transitions have occurred yet, `last_root_hash` returns the hash of the initial abci app's state.
        # `init_chain` will be called between resets when restarting again.
        app_hash = self.context.state.round_sequence.last_round_transition_root_hash
        cast(SharedState, self.context.state).round_sequence.init_chain(message.initial_height)
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_INIT_CHAIN,
            target_message=message,
            validators=ValidatorUpdates(validators),
            app_hash=app_hash,
        )
        return cast(AbciMessage, reply)

    def begin_block(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle the 'begin_block' request."""
        cast(SharedState, self.context.state).round_sequence.begin_block(
            message.header, message.byzantine_validators, message.last_commit_info
        )
        return super().begin_block(message, dialogue)

    def check_tx(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle the 'check_tx' request."""
        transaction_bytes = message.tx
        # check we can decode the transaction
        try:
            transaction = Transaction.decode(transaction_bytes)
            transaction.verify(self.context.default_ledger_id)
            cast(SharedState, self.context.state).round_sequence.check_is_finished()
        except (
            SignatureNotValidError,
            TransactionNotValidError,
            TransactionTypeNotRecognizedError,
        ) as exception:
            self._log_exception(exception)
            return self._check_tx_failed(message, dialogue, exception_to_info_msg(exception))
        except LateArrivingTransaction as exception:  # pragma: nocover
            self.context.logger.debug(exception_to_info_msg(exception))
            return self._check_tx_failed(message, dialogue, exception_to_info_msg(exception))

        # return check_tx success
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_CHECK_TX,
            target_message=message,
            code=OK_CODE,
            data=b"",
            log="",
            info="check_tx succeeded",
            gas_wanted=0,
            gas_used=0,
            events=Events([]),
            codespace="",
        )
        return cast(AbciMessage, reply)

    def settle_pending_offence(self, accused_agent_address: str | None, invalid: bool) -> None:
        """Add an invalid pending offence or a no-offence for the given accused agent address, if possible."""
        if accused_agent_address is None:
            # only add the offence if we know and can verify the sender,
            # otherwise someone could pretend to be someone else, which may lead to wrong punishments
            return

        round_sequence = cast(SharedState, self.context.state).round_sequence

        try:
            last_round_transition_timestamp = timegm(round_sequence.last_round_transition_timestamp.utctimetuple())
        except ValueError:  # pragma: no cover
            # do not add an offence if no round transition has been completed yet
            return

        offence_type = OffenseType.INVALID_PAYLOAD if invalid else OffenseType.NO_OFFENCE
        pending_offense = PendingOffense(
            accused_agent_address,
            round_sequence.current_round_height,
            offence_type,
            last_round_transition_timestamp,
            DEFAULT_PENDING_OFFENCE_TTL,
        )
        round_sequence.add_pending_offence(pending_offense)

    def deliver_tx(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle the 'deliver_tx' request."""
        transaction_bytes = message.tx
        round_sequence = cast(SharedState, self.context.state).round_sequence
        payload_sender: str | None = None
        try:
            transaction = Transaction.decode(transaction_bytes)
            transaction.verify(self.context.default_ledger_id)
            payload_sender = transaction.payload.sender
            round_sequence.check_is_finished()
            round_sequence.deliver_tx(transaction)
        except (
            SignatureNotValidError,
            TransactionNotValidError,
            TransactionTypeNotRecognizedError,
        ) as exception:
            self._log_exception(exception)
            # the transaction is invalid, it's potentially an offence, so we add it to the list of pending offences
            self.settle_pending_offence(payload_sender, invalid=True)
            return self._deliver_tx_failed(message, dialogue, exception_to_info_msg(exception))
        except LateArrivingTransaction as exception:  # pragma: nocover
            self.context.logger.debug(exception_to_info_msg(exception))
            return self._deliver_tx_failed(message, dialogue, exception_to_info_msg(exception))

        # the invalid payloads' availability window needs to be populated with the negative values as well
        self.settle_pending_offence(payload_sender, invalid=False)

        # return deliver_tx success
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_DELIVER_TX,
            target_message=message,
            code=OK_CODE,
            data=b"",
            log="",
            info="deliver_tx succeeded",
            gas_wanted=0,
            gas_used=0,
            events=Events([]),
            codespace="",
        )
        return cast(AbciMessage, reply)

    def end_block(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle the 'end_block' request."""
        self.context.state.round_sequence.tm_height = message.height
        cast(SharedState, self.context.state).round_sequence.end_block()
        return super().end_block(message, dialogue)

    def commit(self, message: AbciMessage, dialogue: AbciDialogue) -> AbciMessage:
        """Handle the 'commit' request.

        As per Tendermint spec (https://github.com/tendermint/spec/blob/038f3e025a19fed9dc96e718b9834ab1b545f136/spec/abci/abci.md#commit):

        Empty request meant to signal to the app it can write state transitions to state.

        - Persist the application state.
        - Return a Merkle root hash of the application state.
        - It's critical that all application instances return the same hash. If not, they will not be able to agree on the next block, because the hash is included in the next block!

        :param message: the ABCI request.
        :param dialogue: the ABCI dialogue.
        :return: the response.
        """
        try:
            cast(SharedState, self.context.state).round_sequence.commit()
        except AddBlockError as exception:
            self._log_exception(exception)
            raise
        # The Merkle root hash of the application state.
        data = self.context.state.round_sequence.root_hash
        # Blocks below this height may be removed. Defaults to 0 (retain all).
        retain_height = 0
        # return commit success
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_COMMIT,
            target_message=message,
            data=data,
            retain_height=retain_height,
        )
        return cast(AbciMessage, reply)

    @classmethod
    def _check_tx_failed(cls, message: AbciMessage, dialogue: AbciDialogue, info: str = "") -> AbciMessage:
        """Handle a failed check_tx request."""
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_CHECK_TX,
            target_message=message,
            code=ERROR_CODE,
            data=b"",
            log="",
            info=info,
            gas_wanted=0,
            gas_used=0,
            events=Events([]),
            codespace="",
        )
        return cast(AbciMessage, reply)

    @classmethod
    def _deliver_tx_failed(cls, message: AbciMessage, dialogue: AbciDialogue, info: str = "") -> AbciMessage:
        """Handle a failed deliver_tx request."""
        reply = dialogue.reply(
            performative=AbciMessage.Performative.RESPONSE_DELIVER_TX,
            target_message=message,
            code=ERROR_CODE,
            data=b"",
            log="",
            info=info,
            gas_wanted=0,
            gas_used=0,
            events=Events([]),
            codespace="",
        )
        return cast(AbciMessage, reply)

    def _log_exception(self, exception: Exception) -> None:
        """Log an exception."""
        self.context.logger.error(exception_to_info_msg(exception))


class AbstractResponseHandler(Handler, ABC):
    """Abstract response Handler.

    This abstract handler works in tandem with the 'Requests' model.
    Whenever a message of 'response' type arrives, the handler
    tries to dispatch it to a pending request previously registered
    in 'Requests' by some other code in the same skill.

    The concrete classes must set the 'allowed_response_performatives'
    class attribute to the (frozen)set of performative the developer
    wants the handler to handle.
    """

    allowed_response_performatives: frozenset[Message.Performative]

    def setup(self) -> None:
        """Set up the handler."""

    def teardown(self) -> None:
        """Tear down the handler."""

    def handle(self, message: Message) -> None:
        """Handle the response message.

        Steps:
        1. Try to recover the 'dialogues' instance, for the protocol
           of this handler, from the skill context. The attribute name used to
           read the attribute is computed by '_get_dialogues_attribute_name()'
           method. If no dialogues instance is found, log a message and return.
        2. Try to recover the dialogue; if no dialogue is present, log a message
           and return.
        3. Check whether the performative is in the set of allowed performative;
           if not, log a message and return.
        4. Try to recover the callback of the request associated to the response
           from the 'Requests' model; if no callback is present, log a message
           and return.
        5. If the above check have passed, then call the callback with the
           received message.

        :param message: the message to handle.
        """
        protocol_dialogues = self._recover_protocol_dialogues()
        if protocol_dialogues is None:
            self._handle_missing_dialogues()
            return
        protocol_dialogues = cast(Dialogues, protocol_dialogues)

        protocol_dialogue = cast(Dialogue | None, protocol_dialogues.update(message))
        if protocol_dialogue is None:
            self._handle_unidentified_dialogue(message)
            return

        if message.performative not in self.allowed_response_performatives:
            self._handle_unallowed_performative(message)
            return

        request_nonce = protocol_dialogue.dialogue_label.dialogue_reference[0]
        ctx_requests = cast(Requests, self.context.requests)

        try:
            callback = cast(
                Callable,
                ctx_requests.request_id_to_callback.pop(request_nonce),
            )
        except KeyError as e:
            msg = f"No callback defined for request with nonce: {request_nonce}"
            raise ABCIAppInternalError(msg) from e

        self._log_message_handling(message)
        current_behaviour = cast(AbstractRoundBehaviour, self.context.behaviours.main).current_behaviour
        callback(message, protocol_dialogue, current_behaviour)

    def _get_dialogues_attribute_name(self) -> str:
        """Get dialogues attribute name.

        By convention, the Dialogues model of the skill follows
        the template '{protocol_name}_dialogues'.

        Override this method accordingly if the name of hte Dialogues
        model is different.

        :return: the dialogues attribute name.
        """
        return cast(PublicId, self.SUPPORTED_PROTOCOL).name + "_dialogues"

    def _recover_protocol_dialogues(self) -> Dialogues | None:
        """Recover protocol dialogues from supported protocol id.

        :return: the dialogues, or None if the dialogues object was not found.
        """
        attribute = self._get_dialogues_attribute_name()
        return getattr(self.context, attribute, None)

    def _handle_missing_dialogues(self) -> None:
        """Handle missing dialogues in context."""
        expected_attribute_name = self._get_dialogues_attribute_name()
        self.context.logger.warning(
            "Cannot find Dialogues object in skill context with attribute name: %s",
            expected_attribute_name,
        )

    def _handle_unidentified_dialogue(self, message: Message) -> None:
        """Handle an unidentified dialogue.

        :param message: the unidentified message to be handled
        """
        self.context.logger.warning("Received invalid message: unidentified dialogue. message=%s", message)

    def _handle_unallowed_performative(self, message: Message) -> None:
        """Handle a message with an unallowed response performative.

        Log an error message saying that the handler did not expect requests
        but only responses.

        :param message: the message
        """
        self.context.logger.warning("Received invalid message: unallowed performative. message=%s.", message)

    def _log_message_handling(self, message: Message) -> None:
        """Log the handling of the message."""
        self.context.logger.debug("Calling registered callback with message=%s", message)


class HttpHandler(AbstractResponseHandler):
    """The HTTP response handler."""

    SUPPORTED_PROTOCOL: PublicId | None = HttpMessage.protocol_id
    allowed_response_performatives = frozenset({HttpMessage.Performative.RESPONSE})


class SigningHandler(AbstractResponseHandler):
    """Implement the transaction handler."""

    SUPPORTED_PROTOCOL: PublicId | None = SigningMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            SigningMessage.Performative.SIGNED_MESSAGE,
            SigningMessage.Performative.SIGNED_TRANSACTION,
            SigningMessage.Performative.ERROR,
        }
    )


class LedgerApiHandler(AbstractResponseHandler):
    """Implement the ledger handler."""

    SUPPORTED_PROTOCOL: PublicId | None = LedgerApiMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            LedgerApiMessage.Performative.BALANCE,
            LedgerApiMessage.Performative.RAW_TRANSACTION,
            LedgerApiMessage.Performative.TRANSACTION_DIGEST,
            LedgerApiMessage.Performative.TRANSACTION_RECEIPT,
            LedgerApiMessage.Performative.ERROR,
            LedgerApiMessage.Performative.STATE,
        }
    )


class ContractApiHandler(AbstractResponseHandler):
    """Implement the contract api handler."""

    SUPPORTED_PROTOCOL: PublicId | None = ContractApiMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            ContractApiMessage.Performative.RAW_TRANSACTION,
            ContractApiMessage.Performative.RAW_MESSAGE,
            ContractApiMessage.Performative.ERROR,
            ContractApiMessage.Performative.STATE,
        }
    )


class TendermintHandler(Handler):
    """The Tendermint config-sharing request / response handler.

    This handler is used to share the information necessary
    to set up the Tendermint network. The agents use it during
    the RegistrationStartupBehaviour, and communicate with
    each other over the Agent Communication Network using a
    p2p_libp2p or p2p_libp2p_client connection.

    This handler does NOT use the ABCI connection.
    """

    SUPPORTED_PROTOCOL: PublicId | None = TendermintMessage.protocol_id

    class LogMessages(Enum):
        """Log messages used in the TendermintHandler."""

        unidentified_dialogue = "Unidentified Tendermint dialogue"
        no_addresses_retrieved_yet = "No registered addresses retrieved yet"
        not_in_registered_addresses = "Sender not registered for on-chain service"
        sending_request_response = "Sending Tendermint request response"
        failed_to_parse_address = "Failed to parse Tendermint network address"
        failed_to_parse_params = "Failed to parse Tendermint recovery parameters from message"
        collected_config_info = "Collected Tendermint config info"
        collected_params = "Collected Tendermint recovery parameters"
        received_error_without_target_message = "Received error message but could not retrieve target message"
        received_error_response = "Received error response"
        sending_error_response = "Sending error response"
        performative_not_recognized = "Performative not recognized"

        def __str__(self) -> str:  # pragma: no cover
            """For ease of use in formatted string literals."""
            return self.value

    def setup(self) -> None:
        """Set up the handler."""

    def teardown(self) -> None:
        """Tear down the handler."""

    @property
    def initial_tm_configs(self) -> dict[str, dict[str, Any]]:
        """A mapping of the other agents' addresses to their initial Tendermint configuration."""
        return self.context.state.initial_tm_configs

    @initial_tm_configs.setter
    def initial_tm_configs(self, configs: dict[str, dict[str, Any]]) -> None:
        """A mapping of the other agents' addresses to their initial Tendermint configuration."""
        self.context.state.initial_tm_configs = configs

    @property
    def dialogues(self) -> TendermintDialogues | None:
        """Tendermint config-sharing request / response protocol dialogues."""

        attribute = cast(PublicId, self.SUPPORTED_PROTOCOL).name + "_dialogues"
        return getattr(self.context, attribute, None)

    def handle(self, message: Message) -> None:
        """Handle incoming Tendermint config-sharing messages."""

        dialogues = cast(TendermintDialogues, self.dialogues)
        dialogue = cast(TendermintDialogue, dialogues.update(message))

        if dialogue is None:
            log_message = self.LogMessages.unidentified_dialogue.value
            self.context.logger.error(f"{log_message}: {message}")
            return

        message = cast(TendermintMessage, message)
        handler_name = f"_{message.performative.value}"
        handler = getattr(self, handler_name, None)
        if handler is None:
            log_message = self.LogMessages.performative_not_recognized.value
            self.context.logger.error(f"{log_message}: {message}")
            return

        handler(message, dialogue)

    def _reply_with_tendermint_error(
        self,
        message: TendermintMessage,
        dialogue: TendermintDialogue,
        error_message: str,
    ) -> None:
        """Reply with Tendermint config-sharing error."""
        response = dialogue.reply(
            performative=TendermintMessage.Performative.ERROR,
            target_message=message,
            error_code=TendermintMessage.ErrorCode.INVALID_REQUEST,
            error_msg=error_message,
            error_data={},
        )
        self.context.outbox.put_message(response)
        log_message = self.LogMessages.sending_error_response.value
        log_message += f". Received: {message}, replied: {response}"
        self.context.logger.error(log_message)

    def _not_registered_error(self, message: TendermintMessage, dialogue: TendermintDialogue) -> None:
        """Check if sender is among on-chain registered addresses."""
        # do not respond to errors to avoid loops
        log_message = self.LogMessages.not_in_registered_addresses.value
        self.context.logger.error(f"{log_message}: {message}")
        self._reply_with_tendermint_error(message, dialogue, log_message)

    def _check_registered(self, message: TendermintMessage, dialogue: TendermintDialogue) -> bool:
        """Check if the sender is registered on-chain and if not, reply with an error."""
        others_addresses = self.context.state.acn_container()
        if message.sender in others_addresses:
            return True

        self._not_registered_error(message, dialogue)
        return False

    def _get_genesis_info(self, message: TendermintMessage, dialogue: TendermintDialogue) -> None:
        """Handler Tendermint config-sharing request message."""

        if not self._check_registered(message, dialogue):
            return
        info = self.initial_tm_configs.get(self.context.agent_address, None)
        if info is None:
            log_message = self.LogMessages.no_addresses_retrieved_yet.value
            self.context.logger.info(f"{log_message}: {message}")
            self._reply_with_tendermint_error(message, dialogue, log_message)
            return

        response = dialogue.reply(
            performative=TendermintMessage.Performative.GENESIS_INFO,
            target_message=message,
            info=json.dumps(info),
        )
        self.context.outbox.put_message(message=response)
        log_message = self.LogMessages.sending_request_response.value
        self.context.logger.info(f"{log_message}: {response}")

    def _get_recovery_params(self, message: TendermintMessage, dialogue: TendermintDialogue) -> None:
        """Handle a request message for the recovery parameters."""
        if not self._check_registered(message, dialogue):
            return

        shared_state = cast(SharedState, self.context.state)
        recovery_params = shared_state.tm_recovery_params
        response = dialogue.reply(
            performative=TendermintMessage.Performative.RECOVERY_PARAMS,
            target_message=message,
            params=json.dumps(asdict(recovery_params)),
        )
        self.context.outbox.put_message(message=response)
        log_message = self.LogMessages.sending_request_response.value
        self.context.logger.info(f"{log_message}: {response}")

    def _genesis_info(self, message: TendermintMessage, dialogue: TendermintDialogue) -> None:
        """Process Tendermint config-sharing response messages."""

        if not self._check_registered(message, dialogue):
            return

        try:  # validate message contains a valid address
            validator_config = json.loads(message.info)
            self.context.logger.info(f"Validator config received: {validator_config}")
            hostname = cast(str, validator_config["hostname"])
            if hostname != "localhost" and not hostname.startswith("node"):
                ipaddress.ip_network(hostname)
        except (KeyError, ValueError) as e:
            log_message = self.LogMessages.failed_to_parse_address.value
            self.context.logger.exception(f"{log_message}: {e} {message}")
            self._reply_with_tendermint_error(message, dialogue, log_message)
            return

        initial_tm_configs = self.initial_tm_configs
        initial_tm_configs[message.sender] = validator_config
        self.initial_tm_configs = initial_tm_configs
        log_message = self.LogMessages.collected_config_info.value
        self.context.logger.info(f"{log_message}: {message}")
        dialogues = cast(TendermintDialogues, self.dialogues)
        dialogues.dialogue_stats.add_dialogue_endstate(
            TendermintDialogue.EndState.COMMUNICATED, dialogue.is_self_initiated
        )

    def _recovery_params(self, message: TendermintMessage, dialogue: TendermintDialogue) -> None:
        """Process params-sharing response messages."""

        if not self._check_registered(message, dialogue):
            return

        try:
            recovery_params = json.loads(message.params)
            shared_state = cast(SharedState, self.context.state)
            shared_state.address_to_acn_deliverable[message.sender] = TendermintRecoveryParams(**recovery_params)
        except (json.JSONDecodeError, TypeError) as exc:
            log_message = self.LogMessages.failed_to_parse_params.value
            self.context.logger.exception(f"{log_message}: {exc} {message}")
            self._reply_with_tendermint_error(message, dialogue, log_message)
            return

        log_message = self.LogMessages.collected_params.value
        self.context.logger.info(f"{log_message}: {message}")
        dialogues = cast(TendermintDialogues, self.dialogues)
        dialogues.dialogue_stats.add_dialogue_endstate(
            TendermintDialogue.EndState.COMMUNICATED, dialogue.is_self_initiated
        )

    def _error(self, message: TendermintMessage, dialogue: TendermintDialogue) -> None:
        """Handle error message as response."""

        target_message = dialogue.get_message_by_id(message.target)
        if not target_message:
            log_message = self.LogMessages.received_error_without_target_message.value
            self.context.logger.error(log_message)
            return

        log_message = self.LogMessages.received_error_response.value
        log_message += f". Received: {message}, in reply to: {target_message}"
        self.context.logger.error(log_message)
        dialogues = cast(TendermintDialogues, self.dialogues)
        dialogues.dialogue_stats.add_dialogue_endstate(
            TendermintDialogue.EndState.NOT_COMMUNICATED, dialogue.is_self_initiated
        )


class IpfsHandler(AbstractResponseHandler):
    """A class for handling IPFS messages."""

    SUPPORTED_PROTOCOL: PublicId | None = IpfsMessage.protocol_id
    allowed_response_performatives = frozenset(
        {
            IpfsMessage.Performative.IPFS_HASH,
            IpfsMessage.Performative.FILES,
            IpfsMessage.Performative.ERROR,
        }
    )
