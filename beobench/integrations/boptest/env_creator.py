"""Module for creating boptest testcases and managing their docker containers"""

import pathlib
import subprocess
import time
import uuid
import docker

try:
    import boptest_gym
except ImportError as error:
    raise ImportError(
        (
            "boptest_gym package is not installed. "
            "You may want to use `installer.py` in the boptest integration"
            "to install BOPTEST including the boptest_gym package."
        )
    ) from error

from beobench.constants import DEFAULT_INSTALL_PATH


def build_testcase(
    testcase: str = "testcase1",
    install_path: pathlib.Path = DEFAULT_INSTALL_PATH,
) -> None:
    """Build a docker image for a BOPTEST testcase.

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
    install_path: pathlib.Path = DEFAULT_INSTALL_PATH,
    add_wait_time: bool = True,
) -> str:
    """Run BOPTEST testcase docker image.

    Args:
        testcase (str, optional): testcase to run. Defaults to "testcase1".
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
    container_name = f"auto_{img_name}_{unique_id}"
    # ip_plus_port = f"127.0.0.1:{local_port}"

    # In order to be able to change the port
    # this command is executed directly
    # without the using the make file.
    print(f"Creating BOPTEST testcase in container named '{container_name}'...")
    args = [
        "docker",
        "run",
        "--name",
        container_name,
        "--rm",
        # "-it",
        # "-p",
        # f"{ip_plus_port}:5000",
        "--network=beobench-net",
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
    # a random free port is allocated.
    # client = docker.from_env()
    # container = client.containers.get(container_name)
    # host_ip = container.ports["5000/tcp"][0]["HostIp"]
    # host_port = container.ports["5000/tcp"][0]["HostPort"]
    # url = f"http://{host_ip}:{host_port}"
    url = f"http://{container_name}:5000"

    print(f"Container created. The BOPTEST API is exposed at '{url}'.")

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
    """Get BOPTEST path from beobench install path.

    Args:
        install_path (str): path of beobench installation.

    Returns:
        pathlib.Path: path to BOPTEST installation.
    """
    return install_path / "boptest"


def create_env(env_config: dict = None) -> boptest_gym.BoptestGymEnv:
    """Create BOPTEST gym environment.

    Args:
        env_config (dict, optional): configuration kwargs of BOPTEST gym.
            Defaults to None.

    Returns:
        boptest_gym.BoptestGymEnv: a gym environment.
    """

    if not env_config:
        env_config = {
            "boptest_testcase": "bestest_hydronic_heat_pump",
            "gym_kwargs": {
                "actions": ["oveHeaPumY_u"],
                "observations": {"reaTZon_y": (280.0, 310.0)},
                "random_start_time": True,
                "max_episode_length": 86400,
                "warmup_period": 10,
                "step_period": 900,
            },
            "normalize": True,
        }

    container_name, url = run_testcase(env_config["boptest_testcase"])
    print("cname", container_name)
    env = boptest_gym.BoptestGymEnv(url=url, **env_config["gym_kwargs"])

    # ensure that the container is stopped once env closed
    def custom_stop_container():
        stop_container(container_name)

    env.close = custom_stop_container

    if "normalize" in env_config and env_config["normalize"] is True:
        env = boptest_gym.NormalizedActionWrapper(env)
        env = boptest_gym.NormalizedObservationWrapper(env)

    if "discretize" in env_config and env_config["discretize"]:
        env = boptest_gym.core.DiscretizedActionWrapper(
            env,
            n_bins_act=env_config["discretize"],
        )

    return env
