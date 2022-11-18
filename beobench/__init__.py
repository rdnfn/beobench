"""Top-level package for beobench."""

__author__ = """Beobench authors"""
__email__ = "-"
__version__ = "0.5.3"

import os
from loguru import logger

from beobench.utils import restart
from beobench.experiment.scheduler import run

# throw error message if trying to use Beobench on windows
if os.name == "nt":
    logger.critical(
        "ERROR: you appear to try to run Beobench directly on Windows. "
        "Beobench CANNOT be run directly on Windows. \n\n"
        "However, you can run Beobench inside Windows Subsystem for Linux (WSL)"
        " on a Windows machine. "
        "See the following link: "
        "https://docs.microsoft.com/en-us/windows/wsl/install. "
        "Beobench will still execute initially but will fail eventually."
    )
