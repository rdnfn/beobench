"""Installer for the different problem defining gym libraries"""

import os

from beobench.constants import (
    DEFAULT_INSTALL_PATH,
    BOPTEST_REPO_URL,
    BOPTEST_REPO_NAME,
    BOPTEST_COMMIT,
)


def install_boptest(install_path: str = DEFAULT_INSTALL_PATH):
    """Install the BOPTEST libraries into the `install_path` directory.

    Args:
        install_path (str, optional): Path of installation.
            Defaults to DEFAULT_INSTALL_PATH.
    """

    # Create installation path directories
    os.makedirs(os.path.dirname(install_path), exist_ok=True)
    # Change to installation path
    os.chdir(DEFAULT_INSTALL_PATH)
    # Clone BOPTEST repo
    os.system(("git clone " + BOPTEST_REPO_URL))
    # Set repo to fixed commit
    os.chdir(BOPTEST_REPO_NAME)
    os.system("git reset --hard " + BOPTEST_COMMIT)
