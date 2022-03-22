"""Module to schedule experiments."""

import os
import uuid
import subprocess
import pathlib
import importlib.util
import warnings
from typing import Union

# RLlib integration is only available inside experiment container
try:
    import beobench.integration.rllib
except ImportError:
    raise ImportError
    print("Note: RLlib beobench integration not available.")


import beobench.experiment.definitions.utils
import beobench.experiment.definitions.default
import beobench.experiment.definitions.methods
import beobench.experiment.definitions.envs
import beobench.experiment.containers
import beobench.experiment.config_parser
import beobench.utils


def run(
    config: Union[str, dict] = None,
    experiment_file: str = None,
    agent_file: str = None,
    method: str = None,
    env: str = None,
    local_dir: str = "./beobench_results/ray_results",
    wandb_project: str = "",
    wandb_entity: str = "",
    wandb_api_key: str = "",
    mlflow_name: str = None,
    use_gpu: bool = False,
    docker_shm_size: str = "2gb",
    no_additional_container: bool = False,
    use_no_cache: bool = False,
    dev_beobench_location: str = None,
) -> None:
    """Run experiment.

    This function allows the use to run experiments from the command line or python
    interface.

    Args:
        config (str or dict, optional): experiment configuration. This can either be
            a dictionary or a path to a yaml file.
        experiment_file (str, optional): File that defines experiment.
            Defaults to None. DEPRECATED.
        agent_file (str, optional): File that defines custom agent. This script is
            executed inside the gym container. DEPRECATED, this should be set in config.
        method (str, optional): RL method to use in experiment. This overwrites any
            method that is set in experiment file. For example 'PPO'. Defaults to None.
        env (str, optional): environment to apply method to in experiment. This
            overwrites any env set in experiment file. Defaults to None.
        local_dir (str, optional): Directory to write experiment files to. This argument
            is equivalent to the `local_dir` argument in `tune.run()`. Defaults to
            `"./beobench_results/ray_results"`.
        wandb_project (str, optional): Name of wandb project. Defaults to
            "initial_experiments".
        wandb_entity (str, optional): Name of wandb entity. Defaults to "beobench".
        wandb_api_key (str, optional): wandb API key. Defaults to None.
        use_gpu (bool, optional): whether to use GPU from the host system. Defaults to
            False.
        mlflow_name (str, optional): name of MLflow experiment.
        docker_shm_size(str, optional): size of the shared memory available to the
            container. Defaults to '2gb'."
        no_additional_container (bool, optional): wether not to start another container
            to run experiments in. Defaults to False, which means that another container
            is started to run experiments in.
        use_no_cache (bool, optional): whether to use cache to build experiment
            container.
        dev_beobench_location (str, optional): github path to beobench package. For
            developement purpose only. This will install a custom beobench version
            inside the experiment container. By default the latest PyPI version is
            installed.
    """
    # pylint: disable=unused-argument

    # get config dict from config argument
    if config:
        config = beobench.experiment.config_parser.parse(config)
    else:
        config = beobench.experiment.config_parser.get_default()
    # Create a definition of experiment from inputs
    if experiment_file is not None:
        warnings.warn(
            "The experiment_file argmunet has been replaced by config",
            DeprecationWarning,
        )
    if agent_file is not None:
        warnings.warn(
            "The agent_file argmunet has been replaced by config",
            DeprecationWarning,
        )

    if config["agent"]["origin"] == "rllib":
        agent_file = None
    else:
        agent_file = pathlib.Path(config["agent"]["origin"])

    # TODO add parsing of high level API arguments env and agent

    if no_additional_container:
        # Execute experiment
        # (this is usually reached from inside an experiment container)

        # run experiment in ray tune

        if config["agent"]["origin"] == "rllib":
            beobench.integration.rllib.run_in_tune(
                config,
                wandb_entity=wandb_entity,
                wandb_project=wandb_project,
                mlflow_name=mlflow_name,
                use_gpu=use_gpu,
            )
        else:
            # run custom RL agent
            args = ["python -m", f"/tmp/beobench/{agent_file.name}"]
            subprocess.check_call(args)

    else:
        # build and run experiments in docker container

        # Ensure local_dir exists, and create otherwise
        local_dir_path = pathlib.Path(local_dir)
        local_dir_path.mkdir(parents=True, exist_ok=True)
        local_dir_abs = str(local_dir_path.absolute())

        # docker setup
        image_tag = beobench.experiment.containers.build_experiment_container(
            build_context=config["env"]["gym"],
            use_no_cache=use_no_cache,
        )

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

        if agent_file is not None:
            ag_file_abs = agent_file.absolute()
            ag_file_on_docker = f"/tmp/beobench/{agent_file.name}"
            docker_flags += [
                "-v",
                f"{ag_file_abs}:{ag_file_on_docker}:ro",
            ]

        # enable docker-from-docker access only for built-in boptest integration.
        if config["env"]["gym"] == "boptest":

            # Create docker network (only useful if starting other containers)
            beobench.experiment.containers.create_docker_network("beobench-net")

            docker_flags += [
                # enable access to docker-from-docker
                "-v",
                "/var/run/docker.sock:/var/run/docker.sock",
                # network allows access to BOPTEST API in other containers
                "--network",
                "beobench-net",
            ]

        # enabling GPU access in docker container
        if use_gpu:
            docker_flags += [
                # add all available GPUs
                "--gpus=all",
            ]

        # define flags for beobench scheduler call inside experiment container
        beobench_flags = []
        beobench_flags.append(f'--config="{config}"')
        if wandb_project:
            beobench_flags.append(f"--wandb-project={wandb_project}")
        if wandb_entity:
            beobench_flags.append(f"--wandb-entity={wandb_entity}")
        if use_gpu:
            beobench_flags.append("--use-gpu")
        beobench_flag_str = " ".join(beobench_flags)

        # if no wandb API key is given try to get it from env
        if not wandb_api_key:
            # this will return "" if env var not set
            wandb_api_key = os.getenv("WANDB_API_KEY", "")

        cmd_list_in_container = [""]
        # dev mode where custom beobench is installed directly from git
        if dev_beobench_location is not None:
            cmd_list_in_container.append("pip uninstall --yes beobench")
            cmd_list_in_container.append(f"pip install {dev_beobench_location}")

        cmd_in_container = " && ".join(cmd_list_in_container)

        args = [
            "docker",
            "run",
            # mount experiment data dir
            "-v",
            f"{local_dir_abs}:/root/ray_results",
            # automatically remove container when stopped/exited
            "--rm",
            # add more memory
            f"--shm-size={docker_shm_size}",
            "--name",
            container_name,
            *docker_flags,
            image_tag,
            "/bin/bash",
            "-c",
            (
                f"export WANDB_API_KEY={wandb_api_key} {cmd_in_container} && "
                f"beobench run {beobench_flag_str} "
                "--no-additional-container && bash"
            ),
        ]
        print("Executing docker command: ", " ".join(args))
        subprocess.check_call(args)


def _create_experiment_def(
    experiment_file: pathlib.Path, method: str, env: str
) -> dict:
    """Create a Beobench experiment definition.

    Args:
        experiment_file (str): path to experiment file.
        method (str): name of RL method.
        env (str): name of environment.
    """
    experiment_def = _load_experiment_file(experiment_file)

    # parsing high level interface options

    # methods
    if method:
        if method == "ppo":
            experiment_def["method"] = beobench.experiment.definitions.methods.PPO
        else:
            raise ValueError(
                (
                    f"The supplied method '{method}' does not match any of "
                    "the pre-configured beobench methods."
                )
            )

    if env:
        if env == "boptest_bestest-hydronic-heat-pump-v1":
            experiment_def["problem"] = getattr(
                beobench.experiment.definitions.envs,
                env.replace("-", "_"),
            )
        if env == "sinergym_eplus-5zone-hot-continous-v1":
            experiment_def["problem"] = getattr(
                beobench.experiment.definitions.envs,
                env.replace("-", "_"),
            )
        if env == "energym_mixed-use-fan-fcu-v0":
            experiment_def["problem"] = getattr(
                beobench.experiment.definitions.envs,
                env.replace("-", "_"),
            )

    return experiment_def


def _load_experiment_file(experiment_file: pathlib.Path) -> dict:
    """Load a Beobench experiment file.

    Args:
        experiment_file (str): path to experiment file.
    """

    # Load experiment definition file
    if experiment_file is None:
        experiment_file_mod = beobench.experiment.definitions.default
    else:
        # import experiment definition file as module
        spec = importlib.util.spec_from_file_location(
            "experiment_definition",
            str(experiment_file.absolute()),
        )
        experiment_file_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(experiment_file_mod)

    experiment_def = {}

    # Create experiment def dictionary, and set default values if not available
    # from experiment_file (module).
    for exp_part in ["problem", "method", "rllib_setup"]:
        if hasattr(experiment_file_mod, exp_part):
            experiment_def[exp_part] = getattr(experiment_file_mod, exp_part)
        else:
            experiment_def[exp_part] = getattr(
                beobench.experiment.definitions.default,
                exp_part,
            )

    return experiment_def
