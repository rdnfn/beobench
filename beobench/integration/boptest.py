"""Module for managing BOPTEST testcase servers"""

import pathlib
import subprocess
import time
import uuid
import docker

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
    local_port: int = 0,
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
        str: name of container
        str: url of testcase API
    """

    img_name = f"boptest_{testcase}"
    unique_id = uuid.uuid4().hex[:6]
    container_name = f"{img_name}_{unique_id}"
    ip_plus_port = f"127.0.0.1:{local_port}"

    # In order to be able to change the port
    # this command is executed directly
    # without the using the make file.
    print(f"Creating boptest testcase in container named '{container_name}'...")
    args = [
        "docker",
        "run",
        "--name",
        f"{container_name}",
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

    # Getting the API port on the host machine.
    # This is necessary because, if local_port is set to 0,
    # a random port is allocated.
    client = docker.from_env()
    container = client.containers.get(container_name)
    host_ip = container.ports["5000/tcp"][0]["HostIp"]
    host_port = container.ports["5000/tcp"][0]["HostPort"]
    url = f"http://{host_ip}:{host_port}"

    print(f"Container created. The boptest API is exposed at '{url}'.")

    return container_name, url


def stop_container(container_name: str) -> None:
    """Stop docker container.

    Args:
        container_name (str): name of docker container to stop.
    """
    client = docker.from_env()
    container = client.containers.get(container_name)
    container.stop(timeout=0)


def _get_boptest_path(install_path: pathlib.Path) -> pathlib.Path:
    """Get boptest path from beobench install path.

    Args:
        install_path (str): path of beobench installation.

    Returns:
        pathlib.Path: path to boptest installation.
    """
    return install_path / "boptest"
