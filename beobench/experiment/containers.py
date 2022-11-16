"""Module for managing experiment containers."""

import contextlib
import subprocess
import os
import docker
from loguru import logger

import beobench
from beobench.constants import AVAILABLE_INTEGRATIONS

# To enable compatiblity with Python<=3.6 (e.g. for sinergym dockerfile)
try:
    import importlib.resources
except ImportError:
    import importlib_resources
    import importlib

    importlib.resources = importlib_resources


def check_image_exists(image: str):
    try:
        client = docker.from_env()
    except docker.errors.DockerException as e:
        logger.error(
            (
                "Unable to access docker client. "
                "Is Docker installed and are all permissions setup? "
                "See here for Beobench installation guidance: "
                "at https://beobench.readthedocs.io/en/latest/getting_started.html. "
                "If on Linux, make sure to follow the post-installation steps to "
                "ensure all necessary permissions are set, see here: "
                "https://beobench.readthedocs.io/en/latest/guides/"
                "installation_linux.html"
            )
        )
        raise e

    try:
        client.images.get(image)
        return True
    except docker.errors.ImageNotFound:
        return False


def build_experiment_container(
    build_context: str,
    use_no_cache: bool = False,
    beobench_package: str = "beobench",
    beobench_extras: str = "extended",
    force_build: bool = False,
    requirements: str = None,
) -> None:
    """Build experiment container from beobench/integrations/boptest/Dockerfile.

    Args:
        build_context (str): context to build from. This can either be a path to
            directory with Dockerfile in it, or a URL to a github repo, or name
            of existing beobench integration (e.g. `boptest`). See the official docs
            https://docs.docker.com/engine/reference/commandline/build/ for more info.
        use_no_cache (bool, optional): wether to use cache in build. Defaults to False.
        beobench_extras (str, optional): which beobench extra dependencies to install
            As in `pip install beobench[extras]`. Defaults to "extended".
        force_build (bool, optional): whether to force a re-build, even if
            image already exists.
    """

    version = beobench.__version__

    # Flags are shared between gym image build and gym_and_beobench image build
    flags = []

    # On arm64 machines force experiment containers to be amd64
    # This is only useful for development purposes.
    # (example: M1 macbooks)
    if os.uname().machine in ["arm64", "aarch64"]:
        # Using buildx to enable platform-specific builds
        build_commands = ["docker", "buildx", "build"]
        flags += ["--platform", "linux/amd64"]
    else:
        # Otherwise use standard docker build command.
        # This change enables usage of older docker versions w/o buildx,
        # e.g. v19.03, on non-arm64 machines
        build_commands = ["docker", "build"]

    if use_no_cache:
        flags.append("--no-cache")

    if build_context in AVAILABLE_INTEGRATIONS:
        image_name = f"beobench_{build_context}"
        gym_name = build_context
        gym_source = importlib.resources.files("beobench").joinpath(
            f"beobench_contrib/gyms/{gym_name}"
        )
        package_build_context = True

        logger.info(f"Recognised integration named {gym_name}.")
    else:
        # get alphanumeric name from context
        context_name = "".join(e for e in build_context if e.isalnum())
        image_name = f"beobench_custom_{context_name}"
        package_build_context = False

    # Create tags of different image stages
    stage0_image_tag = f"{image_name}_base:{version}"
    stage1_image_tag = f"{image_name}_intermediate:{version}"
    stage2_image_tag = f"{image_name}_complete:{version}"

    if requirements is None:
        final_image_tag = stage2_image_tag
    else:
        stage3_image_tag = f"{image_name}_custom_requirements:{version}"
        final_image_tag = stage3_image_tag

    # skip build if image already exists.
    if not force_build and check_image_exists(final_image_tag):
        logger.info(f"Existing image found ({final_image_tag}). Skipping build.")
        return final_image_tag

    logger.warning(
        f"Image not found ({stage2_image_tag}) or forced rebuild. Building image.",
    )

    logger.info(f"Building experiment base image `{stage0_image_tag}`...")

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
        logger.info("Running command: " + " ".join(stage0_build_args))
        subprocess.check_call(
            stage0_build_args,
            env=env,  # this enables accessing dockerfile in subdir
        )

        # Part 2: build stage 1 (intermediate) experiment image
        # This includes installation of beobench in experiment image
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
            logger.info("Running command: " + " ".join(stage1_build_args))
            subprocess.check_call(
                stage1_build_args,
                stdin=proc.stdout,
                env=env,  # this enables accessing dockerfile in subdir
            )

        # Part 3: build stage 2 (complete) experiment image
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

        stage2_dockerfile = str(
            importlib.resources.files("beobench.data.dockerfiles").joinpath(
                f"Dockerfile.beobench_install_{package_type}"
            )
        )

        stage2_build_args = [
            *build_commands,
            "-t",
            stage2_image_tag,
            *stage2_docker_flags,
            "--build-arg",
            f"PREV_IMAGE={stage1_image_tag}",
            "--build-arg",
            f"EXTRAS={beobench_extras}",
            *flags,
            build_context,
        ]

        with subprocess.Popen(
            ["cat", stage2_dockerfile], stdout=subprocess.PIPE
        ) as proc:
            logger.info("Running command: " + " ".join(stage2_build_args))
            subprocess.check_call(
                stage2_build_args,
                stdin=proc.stdout,
                env=env,  # this enables accessing dockerfile in subdir
            )

        if requirements is not None:
            # Part 4: build stage 3 (optional) additional installation of requirements
            build_context = str(requirements.parents[0].absolute())
            # need to add std-in-dockerfile via -f flag and not context directly
            stage3_docker_flags = ["-f", "-"]

            stage3_dockerfile = str(
                importlib.resources.files("beobench.data.dockerfiles").joinpath(
                    "Dockerfile.requirements"
                )
            )

            stage3_build_args = [
                *build_commands,
                "-t",
                stage3_image_tag,
                *stage3_docker_flags,
                "--build-arg",
                f"PREV_IMAGE={stage2_image_tag}",
                "--build-arg",
                f"REQUIREMENTS={requirements.name}",
                *flags,
                build_context,
            ]

            with subprocess.Popen(
                ["cat", stage3_dockerfile], stdout=subprocess.PIPE
            ) as proc:
                logger.info("Running command: " + " ".join(stage3_build_args))
                subprocess.check_call(
                    stage3_build_args,
                    stdin=proc.stdout,
                    env=env,  # this enables accessing dockerfile in subdir
                )

    logger.info("Experiment gym image build finished.")

    return final_image_tag


def create_docker_network(network_name: str) -> None:
    """Create docker network.

    For more details see
    https://docs.docker.com/engine/reference/run/#network-settings

    Args:
        network_name (str): name of docker network.
    """

    logger.info("Creating docker network ...")
    try:
        args = ["docker", "network", "create", network_name]
        subprocess.check_call(args)
        logger.info("Docker network created.")
    except subprocess.CalledProcessError:
        logger.info("No new network created. Network may already exist.")


class DockerSetupError(Exception):
    pass
