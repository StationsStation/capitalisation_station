"""Customized logging for the Derive arbitrage agent."""

# ruff: noqa: D101, D102

import sys
import json
import logging
import importlib
import threading
from queue import Full, Queue
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


def make_handler(handler_cfg: dict, formatter_cfgs: dict) -> logging.Handler:
    """Instantiate a single handler from its config dict."""

    module, clsname = handler_cfg["class"].rsplit(".", 1)
    cls = getattr(importlib.import_module(module), clsname)

    non_init = {"class", "formatter", "level"}
    init_kwargs = {k: v for k, v in handler_cfg.items() if k not in non_init}
    h = cls(**init_kwargs)

    if lvl := handler_cfg.get("level"):
        numeric = getattr(logging, lvl) if isinstance(lvl, str) else lvl
        h.setLevel(numeric)

    fmt = formatter_cfgs[handler_cfg["formatter"]]
    h.setFormatter(make_formatter(fmt))

    return h


class BufferedHandler(logging.Handler):
    def __init__(self, formatter=None, level=logging.NOTSET):
        super().__init__(level=level)
        self._stream = sys.stdout
        self._lock = threading.Lock()
        if formatter:
            self.setFormatter(formatter)

    def emit(self, record):
        try:
            msg = self.format(record)
            with self._lock:
                self._stream.write(msg + "\n")
                self._stream.flush()
        except Exception:  # noqa
            self.handleError(record)


class QueuedHandler(logging.Handler):
    """A handler that enqueues records, and a background QueueListener fans them out to real handlers."""

    def __init__(
        self, queue_size, handler_names, handler_configs, formatter_configs, timeout: float = 0.1, level=logging.NOTSET
    ):
        super().__init__(level=level)

        handlers = (make_handler(handler_configs[name], formatter_configs) for name in handler_names)
        queue = Queue(queue_size)
        self._timeout = timeout
        self._listener = QueueListener(queue, *handlers, respect_handler_level=True)
        self._listener.start()
        self._enqueue = QueueHandler(queue)

    def emit(self, record: logging.LogRecord) -> None:
        """Try to enqueue the record with a bounded timeout. If the queue remains full, fallback to synchronous emit."""
        try:
            self._enqueue.queue.put(record, block=True, timeout=self._timeout)
        except Full:
            # annotate the record so JSONFormatter will include it
            record.synchronous_fallback = True
            # fallback: synchronous emit
            for h in self._real_handlers:
                if record.levelno >= h.level:
                    h.handle(record)

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
