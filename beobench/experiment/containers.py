"""Module for managing experiment containers."""

import subprocess
import os

# To enable compatiblity with Python<=3.6 (e.g. for sinergym dockerfile)
try:
    import importlib.resources
except ImportError:
    import importlib_resources
    import importlib

    importlib.resources = importlib_resources


def build_experiment_container(
    build_context: str,
    use_no_cache: bool = False,
    version="latest",
    enable_rllib=False,
) -> None:
    """Build experiment container from beobench/integrations/boptest/Dockerfile.

    Args:
        build_context (str): context to build from. This can either be a path to
            directory with Dockerfile in it, or a URL to a github repo, or name
            of existing beobench integration (e.g. `boptest`). See the official docs
            https://docs.docker.com/engine/reference/commandline/build/ for more info.
        use_no_cache (bool, optional): wether to use cache in build. Defaults to False.
    """

    # Flags are shared between gym image build and gym_and_beobench image build
    flags = []
    if use_no_cache:
        flags.append("--no-cache")

    AVAILABLE_INTEGRATIONS = [
        "boptest",
        "sinergym",
        "energym",
    ]  # pylint: disable=invalid-name

    if build_context in AVAILABLE_INTEGRATIONS:
        image_name = f"beobench_{build_context}"
        integration_name = build_context
        build_context = (
            f"https://github.com/rdnfn/"
            f"beobench_contrib.git#main:gyms/{build_context}"
        )
        print(
            (
                f"Recognised integration named {integration_name}: using build"
                f" context {build_context}"
            )
        )
    else:
        # get alphanumeric name from context
        context_name = "".join(e for e in build_context if e.isalnum())
        image_name = f"beobench_custom_{context_name}"

    base_image_tag = f"{image_name}_base:{version}"

    print(f"Building experiment base image `{base_image_tag}`...")

    # Part 1: build base experiment image
    args = [
        "docker",
        "build",
        "-t",
        base_image_tag,
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

    # Part 2: build complete experiment image
    # This includes installation of beobench in experiment image
    complete_image_tag = f"{image_name}_complete:{version}"
    complete_dockerfile = str(
        importlib.resources.files("beobench.experiment.dockerfiles").joinpath(
            "Dockerfile.experiment"
        )
    )

    # Which extras to install beobench container
    # e.g. using pip install beobench[extras]
    if enable_rllib:
        beobench_extras = '"extended,rllib"'
    else:
        beobench_extras = "extended"
    # Load dockerfile into pipe
    with subprocess.Popen(["cat", complete_dockerfile], stdout=subprocess.PIPE) as proc:
        beobench_build_args = [
            "docker",
            "build",
            "-t",
            complete_image_tag,
            "-f",
            "-",
            "--build-arg",
            f"GYM_IMAGE={base_image_tag}",
            "--build-arg",
            f"EXTRAS={beobench_extras}",
            *flags,
            build_context,
        ]
        print("Running command: " + " ".join(beobench_build_args))
        subprocess.check_call(
            beobench_build_args,
            stdin=proc.stdout,
            env=env,  # this enables accessing dockerfile in subdir
        )

    print("Experiment gym image build finished.")

    return complete_image_tag


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
