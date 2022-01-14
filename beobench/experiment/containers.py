"""Module for managing experiment containers."""

import subprocess
import os


def build_experiment_container(
    build_context: str, docker_tag: str = None, use_no_cache: bool = False
) -> None:
    """Build experiment container from beobench/integrations/boptest/Dockerfile.

    Args:
        build_context (str): context to build from. This can either be a path to
            directory with Dockerfile in it, or a URL to a github repo, or name
            of existing beobench integration (e.g. `boptest`). See the official docs
            https://docs.docker.com/engine/reference/commandline/build/ for more info.
        use_no_cache (bool, optional): wether to use cache in build. Defaults to False.
    """

    flags = []
    if use_no_cache:
        flags.append("--no-cache")

    AVAILABLE_INTEGRATIONS = ["boptest"]  # pylint: disable=invalid-name

    if build_context in AVAILABLE_INTEGRATIONS:
        docker_tag = f"beobench_{build_context}:latest"
        integration_name = build_context
        build_context = (
            f"https://github.com/rdnfn/"
            f"beobench.git#master:beobench/integrations/{build_context}"
        )
        print(
            (
                f"Recognised integration named {integration_name}: using build"
                f" context {build_context}"
            )
        )
    else:
        if docker_tag is None:
            # get alphanumeric name from context
            context_name = "".join(e for e in build_context if e.isalnum())
            docker_tag = f"beobench_custom_{context_name}:latest"

    print(f"Building experiment container `{docker_tag}`...")

    args = [
        "docker",
        "build",
        "-t",
        docker_tag,
        "-f",
        "Dockerfile",  # change to non-default name
        *flags,
        build_context,
    ]
    env = os.environ.copy()
    env["DOCKER_BUILDKIT"] = "0"
    subprocess.check_call(
        args,
        env=env,  # this enables accessing dockerfile in subdir
    )

    print("Experiment container build finished.")

    return docker_tag


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
