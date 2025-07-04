"""Customized logging for the Derive arbitrage agent."""

# ruff: noqa: D101, D102

import json
import logging


class ShortNameFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord):
        parts = record.name.split(".")
        record.short_name = ".".join(parts[-3:])
        return super().format(record)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        obj = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "name": record.name,
            "pathname": record.pathname,
            "line": record.lineno,
        }
        return json.dumps(obj, ensure_ascii=False)
