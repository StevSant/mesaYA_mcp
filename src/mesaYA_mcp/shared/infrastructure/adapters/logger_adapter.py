"""Logger Adapter - Logging implementation using Python's logging module.

This adapter implements the LoggerPort interface using Python's built-in
logging module, providing structured logging with context and metadata.
"""

import json
import logging
import sys
from typing import Any

from mesaYA_mcp.shared.application.ports.logger_port import LoggerPort


class LoggerAdapter(LoggerPort):
    """Logging adapter using Python's logging module.

    Provides structured JSON logging suitable for production environments
    and MCP server output via stderr.
    """

    def __init__(
        self,
        name: str = "mesaYA_mcp",
        level: int = logging.INFO,
        use_json: bool = True,
    ) -> None:
        """Initialize the logger adapter.

        Args:
            name: Logger name for identification.
            level: Logging level (default: INFO).
            use_json: Whether to use JSON format for logs (default: True).
        """
        self._logger = logging.getLogger(name)
        self._logger.setLevel(level)
        self._use_json = use_json

        # Avoid duplicate handlers
        if not self._logger.handlers:
            handler = logging.StreamHandler(sys.stderr)
            handler.setLevel(level)

            if use_json:
                handler.setFormatter(self._JsonFormatter())
            else:
                handler.setFormatter(
                    logging.Formatter(
                        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
                    )
                )

            self._logger.addHandler(handler)

    class _JsonFormatter(logging.Formatter):
        """JSON formatter for structured logging."""

        def format(self, record: logging.LogRecord) -> str:
            """Format log record as JSON.

            Args:
                record: The log record to format.

            Returns:
                JSON-formatted log string.
            """
            log_data = {
                "timestamp": self.formatTime(record, self.datefmt),
                "level": record.levelname,
                "logger": record.name,
                "message": record.getMessage(),
            }

            # Add extra fields if present
            if hasattr(record, "context") and record.context:
                log_data["context"] = record.context
            if hasattr(record, "meta") and record.meta:
                log_data["meta"] = record.meta
            if hasattr(record, "error") and record.error:
                log_data["error"] = str(record.error)
            if record.exc_info:
                log_data["traceback"] = self.formatException(record.exc_info)

            return json.dumps(log_data, default=str)

    def _log(
        self,
        level: int,
        message: str,
        context: str | None = None,
        error: Exception | None = None,
        **meta: Any,
    ) -> None:
        """Internal logging method with context and metadata.

        Args:
            level: Logging level.
            message: Log message.
            context: Optional context identifier.
            error: Optional exception.
            **meta: Additional metadata.
        """
        extra = {
            "context": context,
            "meta": meta if meta else None,
            "error": error,
        }
        self._logger.log(level, message, extra=extra, exc_info=error is not None)

    def info(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log an informational message.

        Args:
            message: The log message.
            context: Optional context identifier.
            **meta: Additional metadata.
        """
        self._log(logging.INFO, message, context, **meta)

    def warn(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log a warning message.

        Args:
            message: The warning message.
            context: Optional context identifier.
            **meta: Additional metadata.
        """
        self._log(logging.WARNING, message, context, **meta)

    def error(
        self,
        message: str,
        error: Exception | None = None,
        context: str | None = None,
        **meta: Any,
    ) -> None:
        """Log an error message.

        Args:
            message: The error message.
            error: Optional exception instance.
            context: Optional context identifier.
            **meta: Additional metadata.
        """
        self._log(logging.ERROR, message, context, error, **meta)

    def debug(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log a debug message.

        Args:
            message: The debug message.
            context: Optional context identifier.
            **meta: Additional metadata.
        """
        self._log(logging.DEBUG, message, context, **meta)

    def verbose(self, message: str, context: str | None = None, **meta: Any) -> None:
        """Log a verbose message (maps to DEBUG level).

        Args:
            message: The verbose message.
            context: Optional context identifier.
            **meta: Additional metadata.
        """
        self._log(logging.DEBUG, message, context, **meta)
