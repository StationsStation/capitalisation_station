"""Customized logging for the Derive arbitrage agent."""

# ruff: noqa: D101, D102

import json
import logging
import importlib
from queue import Queue
from logging.handlers import QueueHandler, QueueListener


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

        if record.exc_info is not None:
            obj["exc_info"] = self.formatException(record.exc_info)

        if record.stack_info is not None:
            obj["stack_info"] = self.formatStack(record.stack_info)

        # include any extras
        for key, val in record.__dict__.items():
            if key not in LOG_RECORD_BUILTIN_ATTRS:
                obj[key] = val

        return json.dumps(obj, ensure_ascii=False, default=str)


def make_formatter(fmt_cfg: dict) -> logging.Formatter:
    """Instantiate either a stdlib Formatter or a custom one."""

    if "class" in fmt_cfg:
        module, clsname = fmt_cfg["class"].rsplit(".", 1)
        cls = getattr(importlib.import_module(module), clsname)

        # Pass only args the formatter expects (we don't know them all)
        kwargs = {}
        if "format" in fmt_cfg:
            kwargs["fmt"] = fmt_cfg["format"]
        if "datefmt" in fmt_cfg:
            kwargs["datefmt"] = fmt_cfg["datefmt"]
        return cls(**kwargs)

    # Otherwise it's a built-in Formatter
    return logging.Formatter(fmt_cfg.get("format"), datefmt=fmt_cfg.get("datefmt"))


class QueuedHandler(logging.Handler):
    """A handler that enqueues records, and a background QueueListener fans them out to real handlers."""

    def __init__(self, handler_names, handler_configs, formatter_configs, level=logging.NOTSET):
        super().__init__(level=level)

        handlers = []
        non_init_kwargs = {"class", "formatter", "level"}
        for name in handler_names:
            cfg = handler_configs[name]
            module, clsname = cfg["class"].rsplit(".", 1)
            cls = getattr(importlib.import_module(module), clsname)

            init_kwargs = {k: v for k, v in cfg.items() if k not in non_init_kwargs}
            h = cls(**init_kwargs)

            if lvl := cfg.get("level"):
                h.setLevel(getattr(logging, lvl) if isinstance(lvl, str) else lvl)

            fmt = formatter_configs[cfg["formatter"]]
            h.setFormatter(make_formatter(fmt))
            handlers.append(h)

        queue = Queue(-1)
        self._listener = QueueListener(queue, *handlers, respect_handler_level=True)
        self._listener.start()
        self._enqueue = QueueHandler(queue)

    def emit(self, record):
        self._enqueue.emit(record)

    def close(self):
        self._listener.stop()
        super().close()


def _run_benchmark(cfg, n: int = 1_000):
    logging.config.dictConfig(cfg)
    logger = logging.getLogger("aea")
    start = time.perf_counter()
    for i in range(n):
        logger.info("Benchmark message %d", i)

    time.sleep(0.5)  # give listener time to flush
    duration = time.perf_counter() - start
    return f"{n} records in {duration:.3f}s — {n / duration:.0f} msg/s"


if __name__ == "__main__":
    import time
    import logging.config
    from pathlib import Path

    import yaml
    from aea.configurations.base import AgentConfig
    from aea.configurations.loader import ConfigLoader

    base_path = Path(__file__).parent
    aea_config_yaml = base_path / "aea-config.yaml"
    config_loader = ConfigLoader("aea-config_schema.json", AgentConfig)
    agent_config = config_loader.load(aea_config_yaml.read_text())
    cfg = agent_config.logging_config

    n = 10_000
    queue_result = _run_benchmark(cfg, n=n)

    no_queue_config_path = base_path / "no-queue-logging.yaml"
    cfg = yaml.safe_load(no_queue_config_path.read_text())["logging_config"]
    no_queue_result = _run_benchmark(cfg, n=n)

    logger = logging.getLogger("aea")
    logger.info(f"Queue: {queue_result}")
    logger.info(f"No queue: {no_queue_result}")
