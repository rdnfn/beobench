"""Module to schedule experiments."""

from __future__ import annotations

import os
import uuid
import subprocess
import pathlib
import yaml
import contextlib
from typing import Union

# To enable compatiblity with Python<=3.6 (e.g. for sinergym dockerfile)
try:
    import importlib.resources
except ImportError:
    import importlib_resources
    import importlib

    importlib.resources = importlib_resources

import beobench.experiment.containers
import beobench.experiment.config_parser
import beobench.utils
from beobench.constants import CONTAINER_DATA_DIR, CONTAINER_RO_DIR, AVAILABLE_AGENTS


def run(
    config: Union[str, dict, pathlib.Path, list] = None,
    method: str = None,
    env: str = None,
    local_dir: str = None,
    wandb_project: str = None,
    wandb_entity: str = None,
    wandb_group: str = None,
    wandb_api_key: str = None,
    mlflow_name: str = None,
    use_gpu: bool = False,
    docker_shm_size: str = None,
    use_no_cache: bool = False,
    dev_path: str = None,
    no_additional_container: bool = False,
    docker_flags: list[str] = None,
    beobench_extras: str = None,
) -> None:
    """Run experiment.

    This function allows the use to run experiments from the command line or python
    interface.

    Args:
        config (str, dict, pathlib.Path or list, optional): experiment configuration.
            This can either be a dictionary, or a path (str or pathlib) to a yaml file,
            or a json str, or a list combining any number of the prior config types. If
            no config is given, a default config is used.
        method (str, optional): RL method to use in experiment. This overwrites any
            method that is set in experiment file. For example 'PPO'. Defaults to None.
        env (str, optional): environment to apply method to in experiment. This
            overwrites any env set in experiment file. Defaults to None.
        local_dir (str, optional): Directory to write experiment files to. This argument
            is equivalent to the `local_dir` argument in `tune.run()`. Defaults to
            None.
        wandb_project (str, optional): Name of wandb project. Defaults to
            None.
        wandb_entity (str, optional): Name of wandb entity. Defaults to None.
        wandb_group (str, optional): name of wandb run group. Defaults to None.
        wandb_api_key (str, optional): wandb API key. Defaults to None.
        use_gpu (bool, optional): whether to use GPU from the host system. Defaults to
            False.
        mlflow_name (str, optional): name of MLflow experiment. Defaults to None.
        docker_shm_size(str, optional): size of the shared memory available to the
            container. Defaults to None."
        use_no_cache (bool, optional): whether to use cache to build experiment
            container. Defaults to False.
        dev_path (str, optional): file or github path to beobench package. For
            developement purpose only. This will install a custom beobench version
            inside the experiment container. By default the latest PyPI version is
            installed.
        no_additional_container (bool, optional): wether not to start another container
            to run experiments in. Defaults to False, which means that another container
            is started to run experiments in.
        docker_flags (list[str], optional): list of docker flags to be added to
        docker run command of Beobench experiment container.
        beobench_extras (str, optional): extra dependencies to install with beobench.
            Used during pip installation in experiment image, as in using the command:
            `pip install beobench[<beobench_extras>]`
    """
    print("Beobench: starting experiment run ...")
    # parsing relevant kwargs and adding them to config
    kwarg_config = _create_config_from_kwargs(
        local_dir=local_dir,
        wandb_project=wandb_project,
        wandb_entity=wandb_entity,
        wandb_api_key=wandb_api_key,
        wandb_group=wandb_group,
        mlflow_name=mlflow_name,
        use_gpu=use_gpu,
        docker_shm_size=docker_shm_size,
        use_no_cache=use_no_cache,
        dev_path=dev_path,
        docker_flags=docker_flags,
        beobench_extras=beobench_extras,
    )

    # parse combined config
    config = beobench.experiment.config_parser.parse([config, kwarg_config])

    # adding any defaults that haven't been set by user given config
    default_config = beobench.experiment.config_parser.get_default()
    config = beobench.utils.merge_dicts(
        a=default_config, b=config, let_b_overrule_a=True
    )

    autogen_config = beobench.experiment.config_parser.get_autogen_config()
    config = beobench.utils.merge_dicts(
        a=autogen_config, b=config, let_b_overrule_a=True
    )

    # select agent script
    if config["agent"]["origin"] in AVAILABLE_AGENTS:
        agent_file = beobench.experiment.config_parser.get_agent(
            config["agent"]["origin"]
        )
        package_agent = True
    else:
        agent_file = pathlib.Path(config["agent"]["origin"])
        package_agent = False

    # TODO add parsing of high level API arguments env and agent
    if env or method:
        raise ValueError(
            (
                "This functionality has been deprecated. Directly configure"
                " the environment or method in the config argument."
            )
        )

    print(
        (
            f"Beobench: running experiment with environment {config['env']['name']}"
            f" and agent from {config['agent']['origin']}."
        )
    )

    if no_additional_container:
        # Execute experiment
        # (this is usually reached from inside an experiment container)

        container_ro_dir_abs = CONTAINER_RO_DIR.absolute()
        args = ["python", str(container_ro_dir_abs / agent_file.name)]
        subprocess.check_call(args)

    else:
        # build and run experiments in docker container

        ### part 1: build docker images
        # Ensure local_dir exists, and create otherwise
        local_dir_path = pathlib.Path(config["general"]["local_dir"])
        local_dir_path.mkdir(parents=True, exist_ok=True)
        local_dir_path_abs = local_dir_path.absolute()
        container_data_dir_abs = CONTAINER_DATA_DIR.absolute()

        if (
            config["general"]["beobench_extras"] == "extended"
            and config["agent"]["origin"] == "rllib"
        ):
            beobench_extras = "extended,rllib"
        else:
            beobench_extras = config["general"]["beobench_extras"]

        image_tag = beobench.experiment.containers.build_experiment_container(
            build_context=config["env"]["gym"],
            use_no_cache=config["general"]["use_no_cache"],
            beobench_extras=beobench_extras,
            beobench_package=config["general"]["dev_path"],
        )

        ### part 2: create args and run command in docker container
        if config["general"]["docker_flags"] is None:
            docker_flags = []
        else:
            docker_flags = config["general"]["docker_flags"]

        # if no wandb API key is given try to get it from env
        if config["general"]["wandb_api_key"] is None:
            # this will return "" if env var not set
            wandb_api_key = os.getenv("WANDB_API_KEY", "")
        else:
            wandb_api_key = config["general"]["wandb_api_key"]

        # We don't want the key to be logged in wandb
        del config["general"]["wandb_api_key"]

        # Save config to local dir and add mount flag for config
        config_path = local_dir_path / "tmp" / "config.yaml"
        config_path.parent.mkdir(parents=True, exist_ok=True)
        config_path_abs = config_path.absolute()
        config_container_path_abs = (CONTAINER_RO_DIR / "config.yaml").absolute()
        with open(config_path, "w", encoding="utf-8") as conf_file:
            yaml.dump(config, conf_file)
        docker_flags += [
            "-v",
            f"{config_path_abs}:{config_container_path_abs}:ro",
        ]

        # setup container name with unique identifier
        unique_id = uuid.uuid4().hex[:6]
        container_name = f"auto_beobench_experiment_{unique_id}"

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
        if config["general"]["use_gpu"]:
            docker_flags += [
                # add all available GPUs
                "--gpus=all",
            ]

        # define flags for beobench scheduler call inside experiment container
        beobench_flags = []
        beobench_flags.append(f'--config="{config}"')
        beobench_flag_str = " ".join(beobench_flags)

        with contextlib.ExitStack() as stack:
            # if using package agent, get (potentially temp.) agent file path
            if package_agent:
                agent_file = stack.enter_context(
                    importlib.resources.as_file(agent_file)
                )
            # load agent file
            ag_file_abs = agent_file.absolute()
            ag_file_on_docker_abs = (CONTAINER_RO_DIR / agent_file.name).absolute()
            docker_flags += [
                "-v",
                f"{ag_file_abs}:{ag_file_on_docker_abs}:ro",
            ]

            args = [
                "docker",
                "run",
                # mount experiment data dir
                "-v",
                f"{local_dir_path_abs}:{container_data_dir_abs}",
                # automatically remove container when stopped/exited
                "--rm",
                # add more memory
                f"--shm-size={config['general']['docker_shm_size']}",
                "--name",
                container_name,
                *docker_flags,
                image_tag,
                "/bin/bash",
                "-c",
                (
                    f"export WANDB_API_KEY={wandb_api_key} && "
                    f"beobench run {beobench_flag_str} "
                    "--no-additional-container && bash"
                ),
            ]

            arg_str = " ".join(args)
            if wandb_api_key:
                arg_str = arg_str.replace(wandb_api_key, "<API_KEY_HIDDEN>")
            print(f"Executing docker command: {arg_str}")

            subprocess.check_call(args)


def _create_config_from_kwargs(**kwargs) -> dict:
    """Create a config dict from kwargs.

    Returns:
        dict: config dict with kwargs under general key.
    """
    config = {"general": {}}
    for key, value in kwargs.items():
        if value:
            config["general"][key] = value
    return config
