"""Customized logging for the Derive arbitrage agent."""

# ruff: noqa: D101, D102

import logging


class ShortNameFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        parts = record.name.split(".")
        record.short_name = ".".join(parts[-3:])
        return super().format(record)
