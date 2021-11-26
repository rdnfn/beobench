"""Various configuration constants"""

import pathlib

# import os

# Path locations
# DEFAULT_INSTALL_PATH = pathlib.Path(os.getcwd() + "/tmp/beobench_external_install/")
DEFAULT_INSTALL_PATH = pathlib.Path("/opt/beobench")


# REPO URLS
BOPTEST_REPO_URL = "https://github.com/ibpsa/project1-boptest.git"
BOPTEST_REPO_NAME = "project1-boptest"
BOPTEST_COMMIT = "703daf26a9e9e18de7141c021cbfe36aa3578ea8"
BOPTEST_PIP_DEP = ["flask-restful==0.3.9", "pandas==1.3.4", "flask_cors==3.0.10"]

BOPTEST_GYM_REPO_URL = "https://github.com/ibpsa/project1-boptest-gym.git"
BOPTEST_GYM_REPO_NAME = "project1-boptest-gym"
BOPTEST_GYM_COMMIT = "7906edff7c6b7cd521637c110bddd7f26236f3c6"
BOPTEST_GYM_PIP_DEP = [
    "matplotlib",
    "gym",
    "requests",
    "numpy",
    "pandas",
    "scipy",
    "stable-baselines",
]
