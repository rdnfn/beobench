"""Module for managing experiment containers."""

import subprocess
import os


def build_experiment_container(use_no_cache: bool = False) -> None:
    """Build experiment container from beobench/docker/Dockerfile.experiments."""

    print("Building experiment container ...")

    flags = []
    if use_no_cache:
        flags.append("--no-cache")

    args = [
        "docker",
        "build",
        "-t",
        "beobench-experiment:latest",
        "-f",
        "Dockerfile.experiments",  # change to non-default name
        *flags,
        "https://github.com/rdnfn/beobench.git#:docker",
    ]
    env = os.environ.copy()
    env["DOCKER_BUILDKIT"] = "0"
    subprocess.check_call(
        args,
        env=env,  # this enables accessing dockerfile in subdir
    )

    print("Experiment container build finished.")


def create_docker_network(network_name: str) -> None:
    """Create docker network.

    For more details see
    https://docs.docker.com/engine/reference/run/#network-settings

    Args:
        network_name (str): name of docker network.
    """

    print("Creating docker network ...")
    try:
        args = ["docker", "network", "create", network_name]
        subprocess.check_call(args)
        print("Docker network created.")
    except subprocess.CalledProcessError:
        print("No new network created. Network may already exist.")
