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

"""This package contains a scaffold of a model."""

import json
from enum import Enum
from typing import Any, Optional
from dataclasses import dataclass

import pandas as pd
from pydantic import BaseModel as PydanticModel
from sqlalchemy import Float, Column, String, Boolean, BigInteger, create_engine
from sqlalchemy.orm import Session, sessionmaker
from aea.skills.base import Model
from sqlalchemy.ext.declarative import declarative_base

from packages.eightballer.connections.dcxt import PUBLIC_ID as DCXT_PUBLIC_ID
from packages.eightballer.protocols.orders.custom_types import Order, OrderSide, OrderType, OrderStatus
from packages.eightballer.protocols.markets.custom_types import Market
from packages.eightballer.protocols.tickers.custom_types import Ticker
from packages.eightballer.protocols.balances.custom_types import Balance
from packages.eightballer.protocols.positions.custom_types import Position, PositionSide
from packages.eightballer.connections.ccxt_wrapper.connection import PUBLIC_ID as CCXT_PUBLIC_ID


def map_size_to_side(size):
    """Map the size to a side."""
    if size > 0:
        return "long"
    if size < 0:
        return "short"
    return "flat"


@dataclass
class Agent:
    """This class scaffolds an agent."""


@dataclass
class Exchange:
    """This class scaffolds an exchange."""

    type: str


class ExchangeType(Enum):
    """Exchange types."""

    CEX = "cex"
    DEX = "dex"


DEFAULT_EXCHANGES = {
    "lyra": ExchangeType.DEX.value,
    "rysk": ExchangeType.DEX.value,
    "hundred_x": ExchangeType.DEX.value,
    "deribit": ExchangeType.CEX.value,
    "binance": ExchangeType.CEX.value,
    "kraken": ExchangeType.CEX.value,
}


EXCHANGE_TO_PUBLIC_ID = {
    "cex": CCXT_PUBLIC_ID,
    "dex": DCXT_PUBLIC_ID,
}


class ReportingStrategy(Model):
    """This class scaffolds a model."""

    object_to_model = {}
    custom_type_mapping = {
        Order: {OrderStatus, OrderType, OrderSide},
        Position: {
            Optional[PositionSide],  # noqa
        },
    }
    session: Session | None = None
    engine: Any | None = None
    base: Any | None = None
    agent_model: Any | None = None
    _schema: str | None = None

    def setup(self) -> None:
        """Implement the setup."""
        self.context.logger.info("Reporting strategy setting up.")
        self.base = declarative_base()
        for model in [Agent, Exchange, Order, Market, Position, Balance, Ticker]:
            self.object_to_model[model] = self._create_sqlalchemy_model(model)
        self.engine = create_engine(self._connection_string, echo=False)
        self.base.metadata.create_all(self.engine)
        self.session: Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self._add_exchanges()
        # we now confirm we can connect to the database
        self.context.logger.info("Reporting strategy successfully set up.")
        self._schema = "public" if self._connection_string.find("sqlite") == -1 else None

    def _get_agent_model(self):
        """Check if the agent is already in the database, if not add it.
        Use the agent address as the unique identifier.
        """
        with self.session.begin() as session:  # pylint: disable=E1101
            agent = session.query(self.object_to_model[Agent]).first()
            if agent:
                return agent
        return self.get_model(Agent)(
            id=self.context.agent_name,
        )

    def update(self, model, **kwargs) -> None:
        """Implement the registration."""
        with self.session.begin() as session:  # pylint: disable=E1101
            for field, value in kwargs.items():
                setattr(model, field, value)
            session.merge(model)
            session.commit()

    def _add_exchanges(self) -> None:
        """Add exchanges to the database."""
        for name, _type in DEFAULT_EXCHANGES.items():
            new_exchange = self.get_model(Exchange)(
                type=_type,
                id=name,
            )
            self.update(new_exchange)

    def get_model(self, data_class):
        """We make a generic function to get the model for a dataclass."""
        return self.object_to_model[data_class]

    def get_instance(self, data_class_instance, key):
        """Get an instance of a model from a dataclass instance from the database."""
        model = self.get_model(data_class_instance.__class__)
        with self.session.begin() as session:  # pylint: disable=E1101
            instance = session.query(model).filter_by(**{key: getattr(data_class_instance, key)}).first()
        if instance:
            return instance
        return False

    def add_instance(self, data_class_instance):
        """Add an instance of a model from a dataclass instance to the database."""
        model = self.get_model(data_class_instance.__class__)
        instance = model(**json.loads(data_class_instance.json()))
        with self.session.begin() as session:  # pylint: disable=E1101
            session.add(instance)
            session.commit()

    def bulk_add_instances(self, data_class_instances):
        """Add instances of a model from a list of dataclass instances to the database."""
        model = self.get_model(data_class_instances[0].__class__)
        instances = [model(**json.loads(data_class_instance.json())) for data_class_instance in data_class_instances]
        with self.session.begin() as session:  # pylint: disable=E1101
            session.bulk_save_objects(instances)
            session.commit()

    def bulk_update_instances(self, data_class_instances):
        """Update instances of a model from a list of dataclass instances to the database."""
        model = self.get_model(data_class_instances[0].__class__)
        with self.session.begin() as session:  # pylint: disable=E1101
            for data_class_instance in data_class_instances:
                instance = session.query(model).filter_by(id=data_class_instance.id).first()
                data_json = json.loads(data_class_instance.json())
                for field, value in data_json.items():
                    setattr(instance, field, value)
                session.merge(instance)
            session.commit()

    def _create_sqlalchemy_model(self, data_class: PydanticModel) -> Any:
        """Create a sqlalchemy model from pydantic dataclass."""

        class_name = data_class.__name__

        class Model(self.base):
            """This class scaffolds a model."""

            __tablename__ = class_name.lower()
            __table_args__ = {}
            id = Column(String, primary_key=True)

        # add the fields to the model
        for field, _type in data_class.__annotations__.items():
            # skip the id field
            if field == "id":
                continue
            if _type in {Optional[bool], bool}:  # noqa
                setattr(Model, field, Column(Boolean))
            elif _type in {Optional[str], str}:  # noqa
                setattr(Model, field, Column(String))
            elif _type in {Optional[int], int}:  # noqa
                setattr(Model, field, Column(BigInteger))
            elif _type in {Optional[float], float}:  # noqa
                setattr(Model, field, Column(Float))
            elif _type in {Optional[dict[str, Any]], Optional[dict]}:  # noqa
                setattr(Model, field, Column(String))
            elif data_class in self.custom_type_mapping:
                if _type not in self.custom_type_mapping[data_class]:
                    msg = f"Type {_type} not supported for {class_name}.{field}!"
                    raise ValueError(msg)
                # we need to create a relationship here to the custom type...
                setattr(Model, field, Column(String))
            else:
                msg = f"Type {_type} not supported!"
                raise ValueError(msg)
        Model.__name__ = class_name
        return Model

    def __init__(self, **kwargs: Any) -> None:
        """Initialize the model."""
        self._connection_string = kwargs.pop("connection_string")
        if self._connection_string is None:
            msg = "Connection string must be provided!"
            raise ValueError(msg)
        super().__init__(**kwargs)

    def get_markets_data(
        self,
    ) -> list:
        """Get all the markets for an exchange."""
        with self.session.begin() as session:  # pylint: disable=E1101
            markets = session.query(self.object_to_model[Market]).all()

        markets_table = [
            [
                market.strike,
                market.optionType,
                market.expiryDatetime,
                market.symbol,
                market.exchange_id,
            ]
            for market in markets
            if all(
                [
                    market.strike,
                    market.optionType,
                    market.expiryDatetime,
                    market.symbol,
                    market.exchange_id,
                ]
            )
        ]
        markets_columns = [
            "strike",
            "optionType",
            "expiryDatetime",
            "symbol",
            "exchange_id",
        ]
        markets_data = pd.DataFrame(markets_table, columns=markets_columns)
        return markets_data.drop_duplicates()

    def from_positions_to_pivot(self, positions, view="all"):
        """Pivot the positions, creating the following tables:
        - all_positions_pivot
        - deribit_positions_pivot
        - rysk_positions_pivot.
        """
        markets_data = self.get_markets_data()
        if view != "all":
            positions = filter(lambda position: position.exchange_id == view, positions)
        positions_table = [
            [
                position.symbol,
                position.size,
                position.exchange_id,
            ]
            for position in positions
            if all(
                [
                    position.symbol,
                    position.size != 0,
                ]
            )
        ]

        if not positions_table:
            data = pd.DataFrame()
            return self.save_pivot_to_db(data, view)
        positions_columns = ["symbol", "size", "exchange_id"]
        positions_data = pd.DataFrame(positions_table, columns=positions_columns)

        if view != "all":
            positions_data = positions_data.groupby(["symbol", "exchange_id"]).sum().reset_index()
            positions_data["side"] = positions_data["size"].apply(map_size_to_side)
            merged_data = markets_data.merge(positions_data, on=["symbol", "exchange_id"], how="inner")
        else:
            positions_data = (
                positions_data.groupby(
                    [
                        "symbol",
                    ]
                )
                .sum()
                .reset_index()
            )
            positions_data["side"] = positions_data["size"].apply(map_size_to_side)
            merged_data = markets_data.merge(positions_data, on=["symbol"], how="inner")

        merged_data["strike"] = merged_data["strike"].astype(float)
        merged_data["expiryDatetime"] = merged_data["expiryDatetime"].astype(str)
        merged_data["optionType"] = merged_data["optionType"].astype(str)

        pivot_data = pd.pivot_table(
            merged_data,
            values="size",
            index=["strike", "side"],
            columns=["expiryDatetime", "optionType"],
            fill_value=0,
        )
        pivot_data = pivot_data.sort_values(by=["strike"])
        pivot_data = pivot_data.reset_index()
        pivot_data.columns = [f"{i[:10]}_{j}" for i, j in pivot_data.columns]
        return self.save_pivot_to_db(pivot_data, view)

    def save_pivot_to_db(self, pivot_data, view="all"):
        """Save the pivot table to the database."""
        # if no data dont write
        if not len(pivot_data):  # pylint: disable=len-as-condition
            return pivot_data
        with self.session.begin() as session:  # pylint: disable=E1101
            engine = session.get_bind()
            with engine.connect():
                pivot_data.to_sql(
                    f"{view}_positions_pivot",
                    con=engine.raw_connection(),
                    if_exists="replace",
                    schema=self._schema,
                    index=False,
                )
        return pivot_data

    def get_exchanges(self, exchange_type: ExchangeType | None = None):
        """Get the exchanges."""
        query = {}
        if exchange_type:
            query.update({"type": exchange_type.value})
        with self.session.begin() as session:  # pylint: disable=E1101
            exchanges = session.query(self.object_to_model[Exchange]).filter_by(**query).all()
        return [exchange.id for exchange in exchanges]

    def pivot_all_exchanges(self):
        """Pivot the positions for each exchange."""
        for exchange in self.get_exchanges():
            with self.session.begin() as session:  # pylint: disable=E1101
                positions = session.query(self.object_to_model[Position]).filter_by(exchange_id=exchange).all()
            self.from_positions_to_pivot(positions, exchange)

    def pivot_all_positions(self):
        """Pivot the positions for each exchange."""
        with self.session.begin() as session:  # pylint: disable=E1101
            positions = session.query(self.object_to_model[Position]).all()
        self.from_positions_to_pivot(positions, "all")

    def get_orders(self, since=None, status=None, exchange=None, until=None):
        """Get the orders use since to filter by date if provided."""
        # we build our filter, based on whether the user provided any of the optional arguments
        query = {}
        if status:
            query["status"] = status
        if exchange:
            query["exchange_id"] = exchange
        # we now query the database

        with self.session.begin() as session:  # pylint: disable=E1101
            orm_model = self.object_to_model[Order]
            orders = session.query(orm_model).filter_by(**query)
            if since:
                orders = orders.filter(orm_model.latest_update >= since)
            if until:
                orders = orders.filter(orm_model.latest_update <= until)
            return orders.all()

    def get_positions(
        self,
        since=None,
        exchange=None,
        open_only=False,
    ):
        """Get the positions use since to filter by date if provided."""
        # we build our filter, based on whether the user provided any of the optional arguments
        query = {}
        if since:
            query["since"] = since
        if exchange:
            query["exchange_id"] = exchange

        # we now query the database
        with self.session.begin() as session:  # pylint: disable=E1101
            model = self.object_to_model[Position]
            position_query = session.query(model).filter_by(**query)
            if open_only:
                position_query = position_query.filter(model.size != 0)
            return position_query.all()

    def get_balances(self, exchange=None):
        """Gets a snapshot of the balances."""
        # we build our filter, based on whether the user provided any of the optional arguments
        query = {}
        if exchange:
            query["exchange_id"] = exchange
        # we now query the database
        with self.session.begin() as session:  # pylint: disable=E1101
            return session.query(self.object_to_model[Balance]).filter_by(**query).all()
