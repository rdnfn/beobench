"""Module to install different boptest libraries"""

# For python 3.7
from __future__ import annotations

import os
import pathlib
import sys
import click
import subprocess
import warnings

# Constants
DEFAULT_INSTALL_PATH = pathlib.Path("/opt/beobench")


# Repo URLs and dependencies
BOPTEST_REPO_URL = "https://github.com/ibpsa/project1-boptest.git"
BOPTEST_REPO_NAME = "project1-boptest"
BOPTEST_COMMIT = "703daf26a9e9e18de7141c021cbfe36aa3578ea8"
BOPTEST_PIP_DEP = [
    "flask-restful==0.3.9",
    "pandas==1.3.4",
    "flask_cors==3.0.10",
    # BOPTEST gym cannot be added as a direct or extra
    # dependency in setup.py because pypi does not accept
    # such direct dependencies. Therefore it is installed
    # here.
    (
        "boptest_gym@git+"
        "https://github.com/rdnfn/project1-boptest-gym.git@rdnfn/feature-packaging"
    ),
]


@click.command()
@click.option(
    "--install_path", default=DEFAULT_INSTALL_PATH, help="installation path to use"
)
@click.option(
    "--pip_install_dep",
    default=True,
    help="whether to install python dependencies via pip. Defaults to True.",
)
def install(
    install_path: str = DEFAULT_INSTALL_PATH,
    pip_install_dep: bool = True,
):
    """Install the BOPTEST libraries into the `install_path` directory.

    Args:
        install_path (str, optional): Path of installation.
            Defaults to DEFAULT_INSTALL_PATH.
        pip_install_dep (bool, optional): whether to install python dependencies
            via pip. Defaults to True.
    """
    install_path = pathlib.Path(install_path)

    print("Installing BOPTEST...")

    _clone_repo(
        BOPTEST_REPO_URL,
        BOPTEST_REPO_NAME,
        install_path,
        BOPTEST_COMMIT,
        alt_name="boptest",
    )

    if pip_install_dep:
        _install_pip_dependencies(BOPTEST_PIP_DEP)

    # Warning about BOPTEST PYTHONPATH requirement
    boptest_path = install_path / "boptest"
    warnings.warn(
        (
            "In order to use the examples, BOPTEST requires"
            " you to add its repo directory"
            " to the PYTHONPATH variable. This can be done by using the command"
            f" `export PYTHONPATH=$PYTHONPATH:{boptest_path}` before executing"
            " their script."
        ),
    )

    print(f"BOPTEST has been successfully installed at '{boptest_path}'.")


def _clone_repo(
    repo_https_url: str,
    repo_name: str,
    local_path: str = None,
    commit: str = None,
    alt_name: str = None,
) -> None:
    """Clone git repo from https URL, and set it to specific commit.

    Args:
        repo_https_url (str): https URL of repo to clone.
        repo_name (str): default name of repo folder.
        local_path (str, optional): path to clone repo to.
            Defaults to None (current working dir).
        commit (str, optional): commit hash of commit the
            repo should be reset to. Defaults to None (latest commit).
        alt_name (str, optional): name that the local repo
             folder is renamed to. Defaults to None (stay the same).
    """

    local_path = pathlib.Path(local_path)
    os.makedirs(local_path, exist_ok=True)

    try:
        # Clone repo
        with subprocess.Popen(["git", "clone", repo_https_url], cwd=local_path):
            pass

        # Set repo to fixed commit
        with subprocess.Popen(
            ["git", "reset", "--hard", commit], cwd=local_path / repo_name
        ):
            pass

        # Rename repo
        if alt_name is not None:
            print(f"Renaming repo from '{repo_name}' to '{alt_name}'...")
            os.rename(local_path / repo_name, local_path / alt_name)
    except OSError:
        print(
            f"{repo_name} appears to be already installed in '{local_path}'.",
            "Skipping installation.",
        )
    except Exception as e:
        raise e


def _install_pip_dependencies(pip_requirements: list[str]):
    """Install pip dependencies from requirements list.

    Args:
        pip_requirements (list[str]): list of pip requirements.
    """
    print("Installing pip dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *pip_requirements])


if __name__ == "__main__":
    install()
