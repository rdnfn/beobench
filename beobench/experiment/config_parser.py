"""Experiment config parser module"""

from typing import Union
import pathlib
import uuid
import yaml
import ast
import sys

import beobench.utils

# To enable compatiblity with Python<=3.8 (e.g. for sinergym dockerfile)
if sys.version_info[1] >= 9:
    import importlib.resources
else:
    import importlib_resources
    import importlib

    importlib.resources = importlib_resources


def parse(config: Union[dict, str, pathlib.Path, list]) -> dict:
    """Parse experiment config to dict.

    Args:
        config (Union[dict, str, pathlib.Path, list]): path of yaml file

    Returns:
        dict: config in dictionary
    """
    if isinstance(config, list):
        # get list of config dicts
        parsed_configs = []
        for single_config in config:
            parsed_configs.append(parse(single_config))

        # merge config dicts
        parsed_config = {}
        for conf in parsed_configs:
            parsed_config = beobench.utils.merge_dicts(parsed_config, conf)

    elif isinstance(config, pathlib.Path):
        # load config yaml to dict if path given
        with open(config, "r", encoding="utf-8") as config_file:
            parsed_config = yaml.safe_load(config_file)

    elif isinstance(config, str):
        if config[0] in ["{", "["]:
            # if json str or list
            parsed_config = parse(ast.literal_eval(config))
        else:
            # make sure config is a real path
            config_path = pathlib.Path(config)
            parsed_config = parse(config_path)

    elif isinstance(config, dict):
        parsed_config = config

    else:
        raise ValueError(
            f"Config not one of allowed types (dict, str, pathlib.Path, list): {config}"
        )

    return parsed_config


def create_rllib_config(config: dict) -> dict:
    """Create a configuration for ray.tune.run() method.

    Args:
        config (dict): beobench config

    Raises:
        ValueError: this is raised if the config does not specify an rllib agent.

    Returns:
        dict: kwargs for ray.tune.run() method
    """

    # Check if config is with rllib agent
    if config["agent"]["origin"] != "rllib":
        raise ValueError(
            (
                "Configuration does not have rllib agent origin set."
                f"Config is set to: {config}"
            )
        )

    rllib_config = config["agent"]["config"]
    rllib_config["config"]["env_config"] = config["env"]["config"]
    if "name" in config["env"].keys():
        rllib_config["config"]["env"] = config["env"]["name"]
    elif "name" in config["env"]["config"].keys():
        rllib_config["config"]["env"] = config["env"]["config"]["name"]
    else:
        raise ValueError(
            "No name found in config. Either env.name or env.config.name should be set."
        )

    return rllib_config


def get_standard_config(name: str) -> dict:

    """Get standard beobench config from beobench.data.configs

    Returns:
        dict: default beobench config dict
    """

    defs_path = importlib.resources.files("beobench.data.configs")
    with importlib.resources.as_file(defs_path.joinpath(f"{name}.yaml")) as def_file:
        config = parse(def_file)

    return config


def get_default() -> dict:
    """Get default beobench config

    Returns:
        dict: default beobench config dict
    """

    return get_standard_config("default")


def get_agent(name: str) -> pathlib.Path:

    """Get standard beobench agent from beobench.data.agents.

    Returns:
        Path: path/traversible to agent.
    """

    agents_path = importlib.resources.files("beobench.data.agents")
    agent_path = agents_path.joinpath(f"{name}.py")

    return agent_path


def get_autogen_config() -> dict:
    run_id = uuid.uuid4().hex

    config = {"autogen": {"run_id": run_id}}

    return config
