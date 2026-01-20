"""Database module for portfolio value tracking."""

import datetime
from pathlib import Path

from sqlalchemy import Float, Column, DateTime, create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class PortfolioValue(Base):
    """Portfolio value snapshot table."""

    __tablename__ = "value_table"

    datetime = Column(DateTime, primary_key=True)
    total_usd_val = Column(Float, nullable=False)


class PortfolioDatabase:
    """Minimal database handler for portfolio values."""

    def __init__(self, db_config: str = "sqlite:///../data/agent_data.db"):
        """Initialize database connection.

        Args:
        ----
            db_config: Database connection string (SQLite or PostgreSQL)

        """

        if db_config.startswith("sqlite:///"):
            db_path = db_config.replace("sqlite:///", "")
            Path(db_path).parent.mkdir(parents=True, exist_ok=True)

        self.engine = create_engine(
            db_config,
            connect_args={"check_same_thread": False},
        )
        Base.metadata.create_all(self.engine)
        self.SessionLocal = sessionmaker(bind=self.engine)

    def get_session(self) -> Session:
        """Get a new database session."""
        return self.SessionLocal()

    def save_snapshot(self, total_usd: float, timestamp: datetime.datetime | None = None) -> None:
        """Save a portfolio value snapshot.

        Args:
        ----
            total_usd: Total value in USD
            timestamp: Snapshot timestamp (defaults to now)

        """
        if timestamp is None:
            timestamp = datetime.datetime.now(tz=datetime.UTC)

        session = self.get_session()
        try:
            snapshot = PortfolioValue(
                datetime=timestamp,
                total_usd_val=total_usd,
            )
            session.add(snapshot)
            session.commit()
        finally:
            session.close()

    def get_timeseries(
        self,
        column: str = "total_usd_val",
        days: int = 7,
    ) -> list[tuple[datetime.datetime, float]]:
        """Get timeseries data for a specific column.

        Args:
        ----
            column: Column name (default: total_usd_val)
            days: Number of days to look back (default: 7)

        Returns:
        -------
            List of (datetime, value) tuples

        """
        session = self.get_session()
        try:
            cutoff_date = datetime.datetime.now(tz=datetime.UTC) - datetime.timedelta(days=days)

            query = (
                session.query(PortfolioValue.datetime, getattr(PortfolioValue, column))
                .filter(PortfolioValue.datetime >= cutoff_date)
                .order_by(PortfolioValue.datetime.asc())
            )

            return [(row[0], row[1]) for row in query.all()]
        finally:
            session.close()
