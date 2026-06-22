"""Logging setup."""

from __future__ import annotations

import logging

from ..appConfig import settings


def configure_logging() -> None:
    logging.basicConfig(level=settings.log_level)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
