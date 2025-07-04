"""Customized logging for the Derive arbitrage agent."""

# ruff: noqa: D101, D102

import json
import logging


LOG_RECORD_BUILTIN_ATTRS = {
    "args",
    "asctime",
    "created",
    "exc_info",
    "exc_text",
    "filename",
    "funcName",
    "levelname",
    "levelno",
    "lineno",
    "module",
    "msecs",
    "message",
    "msg",
    "name",
    "pathname",
    "process",
    "processName",
    "relativeCreated",
    "stack_info",
    "thread",
    "threadName",
    "taskName",
}


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
            "pathname": record.pathname,
            "line": record.lineno,
        }

        # include any extras
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                obj[key] = val

        return json.dumps(obj, ensure_ascii=False, default=str)
