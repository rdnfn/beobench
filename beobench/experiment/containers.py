"""Module for managing experiment containers."""

import subprocess


def build_experiment_container() -> None:
    """Build experiment container from beobench/docker/Dockerfile.experiments."""

    print("Building experiment container ...")
    args = [
        "DOCKER_BUILDKIT=0",  # this enables accessing dockerfile in subdir
        "docker",
        "build",
        "-t",
        "beobench-experiment:latest",
        "-f",
        "Dockerfile.experiments",  # change to non-default name
        "https://github.com/rdnfn/beobench.git#:docker",
    ]
    subprocess.check_call(args)

    print("Experiment container build finished.")


def create_docker_network(network_name: str) -> None:
    """Create docker network.

    For more details see
    https://docs.docker.com/engine/reference/run/#network-settings

    Args:
        network_name (str): name of docker network.
    """

    print("Creating docker network ...")
    args = ["docker", "network", "create", network_name]
    subprocess.check_call(args)

    print("Docker network created.")
