"""Module for managing experiment containers."""

import contextlib
import subprocess
import os

from beobench.constants import AVAILABLE_INTEGRATIONS

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
    version: str = "latest",
    beobench_package: str = "beobench",
    beobench_extras: str = "extended",
) -> None:
    """Build experiment container from beobench/integrations/boptest/Dockerfile.

    Args:
        build_context (str): context to build from. This can either be a path to
            directory with Dockerfile in it, or a URL to a github repo, or name
            of existing beobench integration (e.g. `boptest`). See the official docs
            https://docs.docker.com/engine/reference/commandline/build/ for more info.
        use_no_cache (bool, optional): wether to use cache in build. Defaults to False.
        version (str, optional): version to add to container tag. Defaults to "latest".
        beobench_extras (str, optional): which beobench extra dependencies to install
            As in `pip install beobench[extras]`. Defaults to "extended".
    """

    # Flags are shared between gym image build and gym_and_beobench image build
    flags = []

    # Using buildx to enable platform-specific builds
    build_commands = ["docker", "buildx", "build"]

    # On arm64 machines force experiment containers to be amd64
    # This is only useful for development purposes.
    # (example: M1 macbooks)
    if os.uname().machine in ["arm64", "aarch64"]:
        flags += ["--platform", "linux/amd64"]

    if use_no_cache:
        flags.append("--no-cache")

    if build_context in AVAILABLE_INTEGRATIONS:
        image_name = f"beobench_{build_context}"
        gym_name = build_context
        gym_source = importlib.resources.files("beobench").joinpath(
            f"beobench_contrib/gyms/{gym_name}"
        )
        package_build_context = True

        print(
            (
                f"Recognised integration named {gym_name}: using build"
                f" context {build_context}"
            )
        )
    else:
        # get alphanumeric name from context
        context_name = "".join(e for e in build_context if e.isalnum())
        image_name = f"beobench_custom_{context_name}"
        package_build_context = False

    stage0_image_tag = f"{image_name}_base:{version}"

    print(f"Building experiment base image `{stage0_image_tag}`...")

    with contextlib.ExitStack() as stack:
        # if using build context from beobench package, get (potentially temp.) build
        # context file path
        if package_build_context:
            build_context = stack.enter_context(importlib.resources.as_file(gym_source))
            build_context = str(build_context.absolute())

        # Part 1: build stage 0 (base) experiment image
        stage0_build_args = [
            *build_commands,
            "-t",
            stage0_image_tag,
            *flags,
            build_context,
        ]
        env = os.environ.copy()
        print("Running command: " + " ".join(stage0_build_args))
        subprocess.check_call(
            stage0_build_args,
            env=env,  # this enables accessing dockerfile in subdir
        )

        # Part 2: build stage 1 (intermediate) experiment image
        # This includes installation of beobench in experiment image
        stage1_image_tag = f"{image_name}_intermediate:{version}"
        stage1_dockerfile = str(
            importlib.resources.files("beobench.data.dockerfiles").joinpath(
                "Dockerfile.experiment"
            )
        )

        stage1_build_args = [
            *build_commands,
            "-t",
            stage1_image_tag,
            "-f",
            "-",
            "--build-arg",
            f"GYM_IMAGE={stage0_image_tag}",
            "--build-arg",
            f"EXTRAS={beobench_extras}",
            *flags,
            build_context,
        ]

        # Load dockerfile into pipe
        with subprocess.Popen(
            ["cat", stage1_dockerfile], stdout=subprocess.PIPE
        ) as proc:
            print("Running command: " + " ".join(stage1_build_args))
            subprocess.check_call(
                stage1_build_args,
                stdin=proc.stdout,
                env=env,  # this enables accessing dockerfile in subdir
            )

        # Part 3: build stage 2 (complete) experiment image
        stage2_dockerfile = str(
            importlib.resources.files("beobench.data.dockerfiles").joinpath(
                "Dockerfile.beobench_install"
            )
        )
        if beobench_package is None:
            beobench_package = "beobench"
        if beobench_package == "beobench":
            package_type = "pypi"
            build_context = "-"
            stage2_docker_flags = []
        else:
            package_type = "local"
            build_context = beobench_package
            # need to add std-in-dockerfile via -f flag and not context directly
            stage2_docker_flags = ["-f", "-"]
        stage2_image_tag = f"{image_name}_complete:{version}"

        stage2_build_args = [
            *build_commands,
            "-t",
            stage2_image_tag,
            *stage2_docker_flags,
            "--build-arg",
            f"PREV_IMAGE={stage1_image_tag}",
            "--build-arg",
            f"PACKAGE={beobench_package}",
            "--build-arg",
            f"PACKAGE_TYPE={package_type}",
            "--build-arg",
            f"EXTRAS={beobench_extras}",
            *flags,
            build_context,
        ]

        with subprocess.Popen(
            ["cat", stage2_dockerfile], stdout=subprocess.PIPE
        ) as proc:
            print("Running command: " + " ".join(stage2_build_args))
            subprocess.check_call(
                stage2_build_args,
                stdin=proc.stdout,
                env=env,  # this enables accessing dockerfile in subdir
            )

    print("Experiment gym image build finished.")

    return stage2_image_tag


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
