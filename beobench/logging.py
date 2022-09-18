"""Logging utilities for Beobench."""

from loguru import logger
import sys


def setup(include_time=False) -> None:
    """Setup Beobench loguru logging setup."""
    if include_time:
        time_str = "<light-black>[{time:YYYY-MM-DD, HH:mm:ss.SSSS}]</light-black> "
    else:
        time_str = ""
    logger.remove()
    logger.level("INFO", color="")
    logger.add(
        sys.stdout,
        colorize=True,
        format=(
            "<blue><b>Beobench</b></blue> "
            "<y>⚡️</y>"
            f"{time_str}"
            "<level>{message}</level>"
        ),
    )


def log_subprocess(pipe, process_name="subprocess"):
    """Log subprocess pipe.

    Adapted from from https://stackoverflow.com/a/21978778.

    Color setting of context is described in https://stackoverflow.com/a/33206814.
    """
    lines = []
    max_len = 1000

    for i, line in enumerate(iter(pipe.readline, b"")):  # b'\n'-separated lines
        context = f"\033[34m{process_name}:\033[0m"  # .decode("ascii")
        line = line.decode("utf-8").rstrip()
        logger.info(f"{context} {line}")
        if i < max_len:
            lines.append(line)
        else:
            lines = lines[1:].append(line)

    output = "\n".join(lines)
    return output
