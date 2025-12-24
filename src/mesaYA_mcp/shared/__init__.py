"""Shared module for common functionality across MCP features."""

from .application import LoggerPort
from .infrastructure import LoggerAdapter

__all__ = ["LoggerPort", "LoggerAdapter"]
