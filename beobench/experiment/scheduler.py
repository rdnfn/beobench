"""Module to schedule experiments."""

import ray.tune
import ray.tune.integration.wandb
import click
import uuid
import subprocess
import pathlib
import importlib.util
import os

import beobench.experiment.definitions.utils
import beobench.experiment.definitions.default
import beobench.experiment.containers
import beobench.utils


def run(
    experiment_file: str = None,
    local_dir: str = "./beobench_results/ray_results",
    wandb_project: str = "",
    wandb_entity: str = "",
    wandb_api_key: str = "",
    no_additional_container: bool = False,
    use_no_cache: bool = False,
) -> None:
    """Run experiment.

    This function allows the use to run experiments from the command line or python
    interface.

    Args:
        experiment_file (str, optional): File that defines experiment.
            Defaults to None.
        local_dir (str, optional): Directory to write experiment files to. This argument
            is equivalent to the `local_dir` argument in `tune.run()`. Defaults to
            `"./beobench_results/ray_results"`.
        wandb_project (str, optional): Name of wandb project. Defaults to
            "initial_experiments".
        wandb_entity (str, optional): Name of wandb entity. Defaults to "beobench".
        wandb_api_key (str, optional): wandb API key. Defaults to None.
        no_additional_container (bool, optional): wether not to start another container
            to run experiments in. Defaults to False, which means that another container
            is started to run experiments in.
        use_no_cache (bool, optional): whether to use cache to build experiment
            container.
    """

    # Load experiment definition file
    if experiment_file is None:
        experiment_def = beobench.experiment.definitions.default
    else:
        experiment_file = pathlib.Path(experiment_file)
        # import experiment definition file as module
        spec = importlib.util.spec_from_file_location(
            "experiment_definition",
            str(experiment_file.absolute()),
        )
        experiment_def = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(experiment_def)

    if no_additional_container:

        # Add wandb callback if sufficient information
        # TODO: add earlier check to see that also API key available
        if wandb_project and wandb_entity:
            callbacks = [_create_wandb_callback(wandb_project, wandb_entity)]
        elif wandb_project or wandb_entity:
            raise ValueError(
                "Only one of wandb_project or wandb_entity given, but both required."
            )
        else:
            callbacks = []
        # run experiment in ray tune
        run_in_tune(
            problem_def=experiment_def.problem,
            method_def=experiment_def.method,
            rllib_setup=experiment_def.rllib_setup,
            rllib_callbacks=callbacks,
        )
    else:
        # build and run experiments in docker container

        # Ensure local_dir exists, and create otherwise
        local_dir_path = pathlib.Path(local_dir)
        local_dir_path.mkdir(parents=True, exist_ok=True)
        local_dir_abs = str(local_dir_path.absolute())

        # docker setup
        image_tag = beobench.experiment.containers.build_experiment_container(
            build_context=experiment_def.problem["problem_library"],
            use_no_cache=use_no_cache,
        )
        beobench.experiment.containers.create_docker_network("beobench-net")

        # define docker arguments/options/flags
        unique_id = uuid.uuid4().hex[:6]
        container_name = f"auto_beobench_experiment_{unique_id}"

        docker_flags = []
        if experiment_file is not None:
            exp_file_abs = experiment_file.absolute()
            exp_file_on_docker = f"/tmp/beobench/{experiment_file.name}"
            docker_flags += [
                "-v",
                f"{exp_file_abs}:{exp_file_on_docker}:ro",
            ]

        # define flags for beobench scheduler call inside experiment container
        beobench_flags = []
        if experiment_file:
            beobench_flags.append(f"--experiment-file={exp_file_on_docker}")
        if wandb_project:
            beobench_flags.append(f"--wandb-project={wandb_project}")
        if wandb_entity:
            beobench_flags.append(f"--wandb-entity={wandb_entity}")
        beobench_flag_str = " ".join(beobench_flags)

        # if no wandb API key is given try to get it from env
        if not wandb_api_key:
            # this will return "" if env var not set
            wandb_api_key = os.getenv("WANDB_API_KEY", "")

        args = [
            "docker",
            "run",
            # the mounted socket allows access to docker
            "-v",
            "/var/run/docker.sock:/var/run/docker.sock",
            # mount experiment data dir
            "-v",
            f"{local_dir_abs}:/root/ray_results",
            # automatically remove container when stopped/exited
            "--rm",
            # network allows access to BOPTEST API in other containers
            "--network",
            "beobench-net",
            # add more memory
            "--shm-size=20.48gb",
            # add available GPUs,
            "--gpus=all",
            "--name",
            container_name,
            *docker_flags,
            image_tag,
            "/bin/bash",
            "-c",
            (
                f"export WANDB_API_KEY={wandb_api_key} && python -m "
                f"beobench.experiment.scheduler {beobench_flag_str} "
                "--no-additional-container && bash"
            ),
        ]
        print("Executing docker command: ", " ".join(args))
        subprocess.check_call(args)


@click.command()
@click.option(
    "--experiment-file",
    default=None,
    help="File that defines beobench experiment.",
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
@click.option(
    "--local-dir",
    default="./beobench_results/ray_results",
    help="Local directory to write results to.",
    type=click.Path(exists=False, file_okay=False, dir_okay=True),
)
@click.option(
    "--wandb-project",
    default="",
    help="Weights and biases project name to log runs to.",
)
@click.option(
    "--wandb-entity",
    default="",
    help="Weights and biases entity name to log runs under.",
)
@click.option(
    "--wandb-api-key",
    default="",
    help="Weights and biases API key.",
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
def run_command(
    experiment_file: str,
    local_dir: str,
    wandb_project: str,
    wandb_entity: str,
    wandb_api_key: str,
    no_additional_container: bool,
    use_no_cache: bool,
) -> None:
    """Run experiment from command line.

    Command line version of run function. This appears to be
    the best (but not great) way to have a parallel python and command
    line interface.

    See https://stackoverflow.com/a/40094408.
    """
    run(
        experiment_file=experiment_file,
        local_dir=local_dir,
        wandb_project=wandb_project,
        wandb_entity=wandb_entity,
        wandb_api_key=wandb_api_key,
        no_additional_container=no_additional_container,
        use_no_cache=use_no_cache,
    )


def run_in_tune(
    problem_def: dict, method_def: dict, rllib_setup: dict, rllib_callbacks: list = None
) -> ray.tune.ExperimentAnalysis:
    """Run beobench experiment.

    Additional info: note that RLlib is a submodule of the ray package, i.e. it is
    imported as `ray.rllib`. For experiment definitions it uses the `ray.tune`
    submodule. Therefore ray tune experiment definition means the same as ray rllib
    experiment defintions. To avoid confusion all variable/argument names use rllib
    instead of ray tune but strictly speaking these are ray tune experiment
    definitions.

    Args:
        problem_def (dict): definition of problem. This is an incomplete
            ray tune experiment defintion that only defines the problem side.
        method_def (dict): definition of method. This is an incomplete
            ray tune experiment defintion that only defines the method side.
        rllib_setup (dict): rllib setup. This is an incomplete
            ray tune experiment defintion that only defines the ray tune/rllib setup
            (e.g. number of workers, etc.).
        rllib_callbacks (list, optional): callbacks to add to ray.tune.run command.
            Defaults to None.

    Returns:
        ray.tune.ExperimentAnalysis: analysis object of completed experiment.
    """
    if rllib_callbacks is None:
        rllib_callbacks = []

    # combine the three incomplete ray tune experiment
    # definitions into a single complete one.
    exp_config = beobench.experiment.definitions.utils.get_experiment_config(
        problem_def, method_def, rllib_setup
    )

    # register the problem environment with ray tune
    # env_creator is a module available in experiment containers
    import env_creator  # pylint: disable=import-outside-toplevel

    ray.tune.registry.register_env(
        problem_def["rllib_experiment_config"]["config"]["env"],
        env_creator.create_env,
    )

    # if run in notebook, change the output reported throughout experiment.
    if beobench.utils.check_if_in_notebook():
        reporter = ray.tune.JupyterNotebookReporter(overwrite=True)
    else:
        reporter = None

    # running the experiment
    analysis = ray.tune.run(
        progress_reporter=reporter,
        callbacks=rllib_callbacks,
        **exp_config,
    )

    return analysis


def _create_wandb_callback(
    wandb_project: str,
    wandb_entity: str,
):
    wandb_callback = ray.tune.integration.wandb.WandbLoggerCallback(
        project=wandb_project, log_config=True, entity=wandb_entity
    )
    return wandb_callback


if __name__ == "__main__":
    run_command()  # pylint: disable=no-value-for-parameter
