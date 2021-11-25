"""Installer for the different problem defining gym libraries"""

import os
import sys
import subprocess
import warnings

from beobench.constants import (
    DEFAULT_INSTALL_PATH,
    BOPTEST_REPO_URL,
    BOPTEST_REPO_NAME,
    BOPTEST_COMMIT,
)


def install_boptest(
    install_path: str = DEFAULT_INSTALL_PATH, pip_install_dep: bool = True
):
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

    # Clean up name
    print("Renaming repo to 'boptest'...")
    new_boptest_path = DEFAULT_INSTALL_PATH / "boptest"
    os.rename(DEFAULT_INSTALL_PATH / BOPTEST_REPO_NAME, new_boptest_path)

    # Install pip dependencies
    if pip_install_dep:
        print("Installing pip dependencies...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pandas"])

    warnings.warn(
        (
            "In order to use the examples, BOPTEST requires"
            " you to add its repo directory"
            " to the PYTHONPATH variable. This can be done by using the command"
            f" `export PYTHONPATH=$PYTHONPATH:{new_boptest_path}` before executing"
            " their script."
        ),
    )

    print(f"BOPTEST has been successfully installed at '{new_boptest_path}'.")
