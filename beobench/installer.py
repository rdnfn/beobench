"""Installer for the different problem defining gym libraries"""

import os
import subprocess

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
    print("Installing BOPTEST")

    # Create installation path directories
    try:
        os.makedirs(install_path)
    except FileExistsError as e:
        raise FileExistsError(
            (
                "It appears that the directory in the install path '%s' already exists."  # pylint: disable=consider-using-f-string
                " Delete the install directory to redo the installation."
            )
            % install_path,
        ) from e
    except Exception as e:
        raise e

    # Clone BOPTEST repo
    with subprocess.Popen(["git", "clone", BOPTEST_REPO_URL], cwd=install_path):
        pass

    # Set repo to fixed commit
    with subprocess.Popen(
        ["git", "reset", "--hard", BOPTEST_COMMIT], cwd=install_path / BOPTEST_REPO_NAME
    ):
        pass

    # clean up name
    os.rename(
        DEFAULT_INSTALL_PATH / BOPTEST_REPO_NAME, DEFAULT_INSTALL_PATH / "boptest"
    )
