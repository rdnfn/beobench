"""Various configuration constants"""

import pathlib
import os

# Path locations
# DEFAULT_INSTALL_PATH = "./tmp/beobench_external_install/"
DEFAULT_INSTALL_PATH = pathlib.Path(os.getcwd() + "/tmp/beobench_external_install/")


# REPO URLS
BOPTEST_REPO_URL = "https://github.com/ibpsa/project1-boptest.git"
BOPTEST_REPO_NAME = "project1-boptest"
BOPTEST_COMMIT = "703daf26a9e9e18de7141c021cbfe36aa3578ea8"
