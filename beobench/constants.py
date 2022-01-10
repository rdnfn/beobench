"""Module with various configuration constants"""

import pathlib

# import os

# Path locations
# DEFAULT_INSTALL_PATH = pathlib.Path(os.getcwd() + "/tmp/beobench_external_install/")
DEFAULT_INSTALL_PATH = pathlib.Path("/opt/beobench")


# REPO URLS
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
