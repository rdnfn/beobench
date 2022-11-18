"""Experiment config parser module"""

from typing import Union
import pathlib
import uuid
import yaml
import ast
import sys
import random
import os
from beobench.logging import logger

import beobench
import beobench.utils

from beobench.constants import USER_CONFIG_PATH

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
    elif (
        config["env"]["config"] is not None and "name" in config["env"]["config"].keys()
    ):
        rllib_config["config"]["env"] = config["env"]["config"]["name"]
    else:
        rllib_config["config"]["env"] = f"default_{config['env']['gym']}_env_name"

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
    """Get default beobench config.

    Returns:
        dict: default beobench config dict
    """

    return get_standard_config("default")


def get_user() -> dict:
    """Get user beobench config.

    Returns:
        dict: default beobench config dict
    """

    if os.path.isfile(USER_CONFIG_PATH):
        logger.info(f"Recognised user config at '{USER_CONFIG_PATH}'.")
        user_config = parse(USER_CONFIG_PATH)
    else:
        user_config = {}

    return user_config


def add_default_and_user_configs(config: dict) -> dict:
    """Add default and user configs to existing beobench config.

    Args:
        config (dict): beobench config

    Returns:
        dict: merged dict of given config, and user and default configs.
    """

    default_config = get_default()
    user_config = get_user()
    user_default_config = beobench.utils.merge_dicts(
        a=default_config, b=user_config, let_b_overrule_a=True
    )
    config = beobench.utils.merge_dicts(
        a=user_default_config, b=config, let_b_overrule_a=True
    )

    return config


def get_autogen_config() -> dict:
    """Get automatically generated parts of a Beobench configuration."""

    config = {
        "autogen": {
            "run_id": uuid.uuid4().hex,
            "random_seed": random.randint(1, 10000000),
        },
    }

    return config


def check_config(config: dict) -> None:
    """Check if config is valid.

    Args:
        config (dict): Beobench config.
    """
    if "version" in config["general"].keys():
        requested_version = config["general"]["version"]
        if requested_version != beobench.__version__:
            raise ValueError(
                f"Beobench config requests version {requested_version}"
                f" that does not match installed version {beobench.__version__}. "
                "Change the installed Beobench version to the requested version "
                f"{requested_version} or remove general.version parameter from config "
                "to prevent this error. "
                "If you have recently changed Beobench version, it may be worth trying"
                " adding the flag `--force-build` to the `beobench run` command. "
                "If you're using Beobench installed from a local clone, also add the "
                "flag `-d <BEOBENCH_REPO_LOCAL_PATH>`."
            )


def get_high_level_config(method: str, gym: str, env: str) -> dict:
    """Get config from agent, gym and env params.

    Args:
        method (str): name of method
        gym (str): name of gym
        env (str): name of environment.

    Returns:
        dict: Beobench configuration.
    """

    config = {}
    if method is not None:
        config = beobench.utils.merge_dicts(
            config,
            get_standard_config(f"method_{method}"),
        )
    if gym is not None and env is not None:
        config = beobench.utils.merge_dicts(
            config,
            get_standard_config(f"gym_{gym}"),
        )
        config["env"]["name"] = env

    return config
