"""Logging utilities for Beobench."""

from loguru import logger
import sys


def setup() -> None:
    """Setup Beobench loguru logging setup."""
    logger.remove()
    logger.add(
        sys.stdout,
        colorize=True,
        format=(
            "<blue>Beobench</blue> "
            "<y>⚡️</y>"
            "<light-black>[{time:YYYY-MM-DD, HH:mm:ss.SSSS}]</light-black> "
            "<level>{message}</level>"
        ),
    )
