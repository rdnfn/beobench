"""Installer for the different problem defining gym libraries"""

import os

from beobench.constants import DEFAULT_INSTALL_PATH



def install_boptest(install_path: str=DEFAULT_INSTALL_PATH):
    """Install the BOPTEST libraries into the `install_path` directory.

    Args:
        install_path (str, optional): Path of installation.
            Defaults to DEFAULT_INSTALL_PATH.
    """

    os.chdir(DEFAULT_INSTALL_PATH)
    os.system("git clone https://github.com/ibpsa/project1-boptest")

    return None
