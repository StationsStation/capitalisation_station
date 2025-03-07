# ------------------------------------------------------------------------------
#
#   Copyright 2023 eightballer
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

"""This package contains a scaffold of a behaviour."""

import datetime
from typing import Any, cast

from aea.skills.behaviours import TickerBehaviour

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.skills.reporting.slack import SlackUploader
from packages.eightballer.protocols.orders.message import OrdersMessage
from packages.eightballer.skills.reporting.strategy import DEFAULT_EXCHANGES, ExchangeType, ReportingStrategy
from packages.eightballer.protocols.orders.dialogues import OrdersDialogue, OrdersDialogues
from packages.eightballer.protocols.positions.message import PositionsMessage
from packages.eightballer.protocols.orders.custom_types import Order, OrderStatus
from packages.eightballer.protocols.positions.dialogues import PositionsDialogue
from packages.eightballer.connections.ccxt_wrapper.connection import PUBLIC_ID as CCXT_PUBLIC_ID
from packages.eightballer.connections.ccxt_wrapper.interfaces.order import (
    from_id_to_instrument_name as base_from_id_to_instrument_name,
)


from_id_to_instrument_name = base_from_id_to_instrument_name


SYSTEM_TZ = datetime.datetime.now().astimezone().tzinfo


def from_instrument_name_to_id(instrument_name):
    """Simple helper function to convert instrument name to id.
    input:
        ETH/USD:ETH-231027-2000-C
        ETH/USD:ETH-231027-2000-P.

    output:
       "ETH-27OCT23-2000-C"
    """

    parts = instrument_name.split(":")
    if len(parts) != 2:
        msg = f"Invalid instrument name: {instrument_name}"
        raise ValueError(msg)
    symbol = parts[1]
    # we now need to extract the date and strike
    parts = symbol.split("-")
    if len(parts) != 4:
        msg = f"Invalid instrument name: {instrument_name}"
        raise ValueError(msg)
    date = parts[1]
    year = date[:2]
    month = date[2:4]
    day = date[4:]
    # we need to pad the day with a  if it's a single digit
    date_obj = datetime.datetime.strptime(  # noqa
        str(month),
        "%m",
    )
    month = date_obj.strftime("%b").upper()
    if int(day) < 10:
        day = f"0{day}"
    date = f"{day}{month}{year}"
    return f"{parts[0]}-{date}-{parts[2]}-{parts[3]}"


class EodReportingBehaviour(TickerBehaviour):
    """This class scaffolds a behaviour."""

    enabled: bool
    interval: int
    daily_report_times: list[datetime.time]
    uploader: Any
    _reported_today: dict[str, datetime.date] = {}

    def setup(self) -> None:
        """Implement the setup."""

    def _run_reports(self, report_time: datetime.time) -> None:
        """Run the reports for the given time."""
        self.context.logger.info(f"Running reports for {report_time}")
        # get the data
        # format the data
        # upload the data (if enabled)
        # set the next report time
        strategy = cast(ReportingStrategy, self.context.reporting_strategy)

        balances = strategy.get_balances()
        self.context.logger.info(f"Balances: {balances}")

        # we now format it.
        cols = ["latest_update", "asset_id", "exchange_id", "free", "used", "total"]
        data = [cols]

        def get_cols_from_model(columns, model):
            row_data = []
            for column in columns:
                val = getattr(model, column)
                if isinstance(val, datetime.datetime):
                    val = val.isoformat()
                row_data.append(val)
            return row_data

        for balance in balances:
            data.append(get_cols_from_model(cols, balance))
        self.context.logger.info(f"Order Data: {data}")

        msg, _ = self.uploader.upload(
            self.context.http_dialogues,
            data,
            f"{report_time.strftime('%Y-%m-%d')}_balances.csv",
        )
        self.context.logger.info(f"Message: {msg}")
        self.context.outbox.put_message(
            message=msg,
        )

        fills = strategy.get_orders(
            status=OrderStatus.FILLED.name,
            since=report_time - datetime.timedelta(days=1),
            until=report_time,
        )
        self.context.logger.debug(f"Fills: {fills}")

        # we now format it.
        cols = [
            "latest_update",
            "exchange_id",
            "id",
            "type",
            "side",
            "price",
            "amount",
            "filled",
            "status",
            "datetime",
            "fees",
        ]
        data = [cols]
        for fill in fills:
            data.append(get_cols_from_model(cols, fill))
        self.context.logger.info(f"Data: {data}")

        # we now set the next report time
        msg, _ = self.uploader.upload(
            self.context.http_dialogues,
            data,
            f"{report_time.strftime('%Y-%m-%d')}_fills.csv",
        )
        self.context.outbox.put_message(
            message=msg,
        )

    def teardown(self) -> None:
        """Implement the task teardown."""

    def get_report_time(self, report_time: datetime.time) -> datetime.datetime:
        """Takes report time and gets the next datetime of the report. Returns none if not ready."""
        now = datetime.datetime.now(tz=SYSTEM_TZ)
        if now >= report_time:
            return report_time + datetime.timedelta(days=1)
        return None

    def act(self) -> None:
        """For each daily report time, check if it's time to report and report if so
        create the report;
        - get the data
        - format the data
        - upload the data (if enabled)
        - set the next report time.

        We have a list of report times, then a map of the next time they are scheduled to run.
        so we need to check if we've already reported today
        and if not, check if it's time to report and report if so.
        """
        if not self.daily_report_enabled:
            return
        done_reports = []
        new_report_times = []
        for report_time in self.report_times:
            next_report_time = self.get_report_time(report_time)
            if next_report_time is not None:
                self._run_reports(report_time)
                # set the next report time
                self.context.logger.info(f"Setting next report time: {next_report_time}")
                new_report_times.append(next_report_time)
                # mark this report as done
                self.context.logger.info(f"Marking report as done: {report_time}")
                done_reports.append(report_time)
        for done_report in done_reports:
            self.report_times.remove(done_report)
        # add the new report times
        for new_report_time in new_report_times:
            self.report_times.append(new_report_time)

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the behaviour."""
        interval = kwargs.pop("interval")
        daily_report_times = kwargs.pop("daily_report_times")
        self.report_times = []
        for daily_report_time in daily_report_times:
            yesterday = datetime.datetime.now(tz=SYSTEM_TZ) - datetime.timedelta(days=1)
            report_time = datetime.time.fromisoformat(daily_report_time)
            yesterdays_report_time = yesterday.replace(
                hour=report_time.hour,
                minute=report_time.minute,
                second=report_time.second,
            )
            self.report_times.append(yesterdays_report_time)
        self.daily_report_enabled = kwargs.pop("daily_report_enabled")
        super().__init__(tick_interval=interval, **kwargs)

        uploader = kwargs.pop("uploader")
        config = uploader["config"]
        config["agent_address"] = self.context.agent_address

        if uploader["class_name"] == SlackUploader.__name__:
            self.uploader = SlackUploader(**config)
        else:
            msg = f"Unknown uploader class: {uploader['class_name']}"
            raise ValueError(msg)

        self.context.logger.info(f"Reporting Uploader: {self.uploader}")
        self.context.logger.info(f"Reporting Uploader Daily Report Times: {self.report_times}")


class ReconciliationBehaviour(TickerBehaviour):
    """Reconciliation Behaviour.

    The behaviour will:
    -> check the database for any orders that are open.
    -> check check against the exchange for the status of those orders.
    -> if the order status has changed, update the database wth the new status.
    """

    enabled: bool = True
    currency: str = "ETH"
    start_timestamp: float = 0.0
    last_settlement_check: float = 0.0

    def __init__(self, **kwargs) -> None:
        """Initialize the behaviour."""
        self.currency = kwargs.pop("currency")
        self.enabled = kwargs.pop("enabled")
        self.last_settlement_check = float(kwargs.pop("start_timestamp"))

        super().__init__(tick_interval=kwargs.pop("interval"), **kwargs)

    @property
    def strategy(self) -> ReportingStrategy:
        """Get the strategy."""
        return cast(ReportingStrategy, self.context.reporting_strategy)

    def act(self) -> None:
        """Implement the act."""
        if not self.enabled:
            return
        open_orders = self.strategy.get_orders(status=OrderStatus.OPEN.name)

        self.context.logger.info(f"Open Orders: {open_orders}")

        for open_order in open_orders:
            # we here need to submit a request to the exchange to get the order status
            self.context.logger.info(f"Checking order status: {open_order}")
            self.check_order_status(open_order)

        exchange_positions = {}
        for cex_exchange in self.strategy.get_exchanges(exchange_type=ExchangeType.CEX):
            exchange_positions[cex_exchange] = self.strategy.get_positions(
                exchange=cex_exchange,
                open_only=True,
            )

        for exchange_id, positions in exchange_positions.items():
            for position in positions:
                self.check_position_status(position, exchange_id)
        #  we also need to check the settled trades
        for exchange_id in exchange_positions:
            self.check_settlements(exchange_id)

    def check_order_status(self, order: Order) -> None:
        """We send a messsage to the ccxt connection."""
        dialogues = cast(OrdersDialogue, self.context.orders_dialogues)
        target_id = self.get_target_id(order.exchange_id)
        msg, _ = dialogues.create(
            counterparty=str(target_id),
            performative=OrdersMessage.Performative.GET_ORDER,
            order=order,
            exchange_id=order.exchange_id,
        )
        self.context.outbox.put_message(msg)

    def check_position_status(self, position: Any, exchange_id) -> None:
        """We send a messsage to the ccxt connection."""
        dialogues = cast(PositionsDialogue, self.context.positions_dialogues)

        # we need to do a little bit of parsing here to get the symbol unfortunately. WTF CCXT?
        #

        symbol = from_instrument_name_to_id(position.symbol)
        target_id = self.get_target_id(exchange_id)

        msg, _ = dialogues.create(
            counterparty=target_id,
            performative=PositionsMessage.Performative.GET_POSITION,
            position_id=symbol,
            exchange_id=exchange_id,
        )
        self.context.outbox.put_message(msg)

    def get_target_id(self, exchange_id: str) -> str:
        """Get the target id."""
        exchange_type: ExchangeType = DEFAULT_EXCHANGES[exchange_id]
        if exchange_type == ExchangeType.DEX.value:
            target_id = DCXT_PUBLIC_ID
        elif exchange_type == ExchangeType.CEX.value:
            target_id = CCXT_PUBLIC_ID
        else:
            msg = f"Unknown exchange type: {exchange_type}"
            raise ValueError(msg)
        return str(target_id)

    def check_settlements(self, exchange_id) -> None:
        """Check the settlements for the exchange."""

        dialogues = cast(OrdersDialogues, self.context.orders_dialogues)
        current_timestamp = float(datetime.datetime.now(tz=SYSTEM_TZ).timestamp())
        target_id = self.get_target_id(exchange_id)

        msg, _ = dialogues.create(
            counterparty=str(target_id),
            performative=OrdersMessage.Performative.GET_SETTLEMENTS,
            exchange_id=exchange_id,
            start_timestamp=self.last_settlement_check,
            end_timestamp=current_timestamp,
            currency=self.currency,
        )
        self.context.outbox.put_message(msg)
        self.last_settlement_check = current_timestamp
