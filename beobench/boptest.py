"""Module for managing BOPTEST testcase servers"""

import pathlib
import subprocess
import time

from beobench.constants import DEFAULT_INSTALL_PATH


def build_testcase(
    testcase: str = "testcase1",
    install_path: pathlib.Path = DEFAULT_INSTALL_PATH,
) -> None:
    """Build a docker image for a BOPTEST tescase.

    A built image is required before running a testcase.

    Args:
        testcase (str, optional): testcase name. Defaults to "testcase1".
        install_path (pathlib.Path, optional): path of beobench installation.
            Defaults to DEFAULT_INSTALL_PATH.
    """

    subprocess.check_call(
        ["make", "build", f"TESTCASE={testcase}"],
        cwd=_get_boptest_path(install_path),
    )


def run_testcase(
    testcase: str = "testcase1",
    local_port: int = 5000,
    install_path: pathlib.Path = DEFAULT_INSTALL_PATH,
    add_wait_time: bool = True,
) -> str:
    """Run BOPTEST testcase docker image.

    Args:
        testcase (str, optional): testcase to run. Defaults to "testcase1".
        local_port (int, optional): port on local machine for experiment API.
            Defaults to 5000.
        install_path (pathlib.Path, optional): path of beobench installation.
            Defaults to DEFAULT_INSTALL_PATH.
        add_wait_time (bool, optional): wether to add some wait time for
            API in container to get ready. This is useful when after this
            command the API is immidiately accessed. Defaults to True.

    Returns:
        str: url of testcase API
    """

    img_name = f"boptest_{testcase}"
    ip_plus_port = f"127.0.0.1:{local_port}"
    url = f"http://{ip_plus_port}"

    # In order to be able to change the port
    # this command is executed directly
    # without the using the make file.
    args = [
        "docker",
        "run",
        "--name",
        f"{img_name}",
        "--rm",
        # "-it",
        "-p",
        f"{ip_plus_port}:5000",
        "--detach=true",
        img_name,
        "/bin/bash",
        "-c",
        "python restapi.py && bash",
    ]

    subprocess.check_call(
        args,
        cwd=_get_boptest_path(install_path),
    )

    if add_wait_time:
        # Allow for the docker image to launch
        time.sleep(5)

    return url


def stop_testcase(
    testcase: str = "testcase1", install_path: pathlib.Path = DEFAULT_INSTALL_PATH
) -> None:
    """Stop currently running testcase.

    Args:
        testcase (str, optional): testcase to stop. Defaults to "testcase1".
        install_path (pathlib.Path, optional): path of beobench installation.
            Defaults to DEFAULT_INSTALL_PATH.
    """

    subprocess.check_call(
        ["make", "stop", f"TESTCASE={testcase}"],
        cwd=_get_boptest_path(install_path),
    )


def _get_boptest_path(install_path: pathlib.Path) -> pathlib.Path:
    """Get boptest path from beobench install path.

    Args:
        install_path (str): path of beobench installation.

    Returns:
        pathlib.Path: path to boptest installation.
    """
    return install_path / "boptest"
