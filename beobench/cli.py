"""Command line interface for beobench."""

import click

import beobench.experiment.scheduler
import beobench.experiment.containers
import beobench.utils


@click.group()
def cli():
    """Command line interface for Beobench."""


@cli.command()
@click.option(
    "--config",
    "-c",
    default=None,
    help="Json or filepath with yaml that defines beobench experiment configuration.",
    type=str,
    multiple=True,
)
@click.option(
    "--method",
    default=None,
    help="Name of RL method to use in experiment.",
)
@click.option(
    "--gym",
    default=None,
    help="Name of gym framework to use in experiment.",
)
@click.option(
    "--env",
    default=None,
    help="Name of RL environment to use in experiment.",
)
@click.option(
    "--local-dir",
    default=None,
    help="Local directory to write results to.",
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
)
@click.option(
    "--wandb-project",
    default=None,
    help="Weights and biases project name to log runs to.",
)
@click.option(
    "--wandb-entity",
    default=None,
    help="Weights and biases entity name to log runs under.",
)
@click.option(
    "--wandb-api-key",
    default=None,
    help="Weights and biases API key.",
)
@click.option(
    "--mlflow-name",
    default=None,
    help="Name of MLflow experiment.",
)
@click.option(
    "--use-gpu",
    is_flag=True,
    help="Whether to use GPUs from the host system in experiment container.",
)
@click.option(
    "--docker-shm-size",
    default=None,
    help="Size of shared memory available to experiment container.",
)
@click.option(
    "--no-additional-container",
    is_flag=True,
    help="Do not run another container to do experiments in.",
)
@click.option(
    "--use-no-cache",
    is_flag=True,
    help="Whether to use cache to build experiment container.",
)
@click.option(
    "--dev-path",
    "-d",
    default=None,
    help="For developer use only: location of custom beobench package version.",
)
@click.option(
    "--force-build",
    is_flag=True,
    help="Whether to force a re-build, even if image already exists.",
)
@click.option(
    "--dry-run",
    is_flag=True,
    help=(
        "Whether to dry run the experiment without"
        " running docker commands/saving files."
    ),
)
@click.option(
    "--registry",
    default=None,
    help=(
        "Registry to take Beobench experiment container images from."
        " Defaults to empty string, which is Docker Hub"
    ),
    type=str,
)
@click.option(
    "--use-registry",
    is_flag=True,
    help="Whether to use container from registry, and not build container locally.",
)
def run(
    config: str,
    method: str,
    gym: str,
    env: str,
    local_dir: str,
    wandb_project: str,
    wandb_entity: str,
    wandb_api_key: str,
    mlflow_name: str,
    use_gpu: bool,
    docker_shm_size: str,
    no_additional_container: bool,
    use_no_cache: bool,
    dev_path: str,
    force_build: bool,
    dry_run: bool,
    registry: str,
    use_registry: bool,
) -> None:
    """Run beobench experiment from command line.

    Command line version of beobench.run() function.
    """

    # This appears to be the best (but not great) way to have a parallel python
    # and command line interface.
    #
    # See https://stackoverflow.com/a/40094408.

    beobench.experiment.scheduler.run(
        config=list(config),
        method=method,
        gym=gym,
        env=env,
        local_dir=local_dir,
        wandb_project=wandb_project,
        wandb_entity=wandb_entity,
        wandb_api_key=wandb_api_key,
        mlflow_name=mlflow_name,
        use_gpu=use_gpu,
        docker_shm_size=docker_shm_size,
        no_additional_container=no_additional_container,
        use_no_cache=use_no_cache,
        dev_path=dev_path,
        force_build=force_build,
        dry_run=dry_run,
        registry=registry,
        use_registry_container=use_registry,
    )


@cli.command()
def restart():
    """Restart beobench. This will stop any remaining running beobench containers."""
    beobench.utils.restart()


@cli.command()
@click.option(
    "--build-context",
    "-b",
    default=None,
    help=(
        "Context to build from. This can either be a path to"
        "directory with Dockerfile in it, or a URL to a github repo, or name"
        "of existing beobench integration (e.g. `boptest`)."
    ),
    type=str,
)
@click.option(
    "--registry",
    default=None,
    help=("Registry to push to."),
    type=str,
)
@click.option(
    "--push-image",
    is_flag=True,
    help=("Whether to push image to registry."),
)
@click.option(
    "--enable-dockerhub-cache",
    is_flag=True,
    help=("Whether to push image to registry."),
)
@click.option(
    "--beobench-package",
    default=None,
    help=("Path of Beobench package (if using local package)."),
    type=str,
)
@click.option(
    "--beobench-extras",
    default="extended,rllib,sb3",
    help="Extra dependencies to install for Beobench package.",
    type=str,
)
@click.option(
    "--img-name-appendix",
    default="",
    help="String to add to image tag name.",
    type=str,
)
@click.option(
    "--extras-mode",
    default=None,
    help="Beobench extras mode.",
    type=str,
)
def build_experiment_container(
    build_context: str,
    registry: str,
    push_image: bool,
    enable_dockerhub_cache: bool,
    beobench_package: str,
    img_name_appendix: str,
    beobench_extras: str,
    extras_mode: str,
):
    """Build experiment container"""

    if extras_mode == "standard":
        beobench_extras = "extended,rllib,sb3"
        img_name_appendix = ""
    if extras_mode == "light":
        beobench_extras = "extended"
        img_name_appendix = "_light"

    beobench.experiment.containers.build_experiment_container(
        build_context=build_context,
        registry=registry,
        push_image=push_image,
        enable_dockerhub_cache=enable_dockerhub_cache,
        beobench_package=beobench_package,
        img_name_appendix=img_name_appendix,
        beobench_extras=beobench_extras,
    )
