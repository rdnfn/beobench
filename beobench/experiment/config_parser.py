"""Experiment config parser module"""

from typing import Union
import pathlib
import yaml


def parse(config: Union[str, pathlib.Path]) -> dict:
    """Parse experiment config from yaml file to dict.

    Args:
        config (Union[str, pathlib.Path]): path of yaml file

    Returns:
        dict: config in dictionary
    """

    # load config dict if path given
    if isinstance(config, (str, pathlib.Path)):
        # make sure config is a real path
        if isinstance(config, str):
            config = pathlib.Path(config)
        with open(config, "r", encoding="utf-8") as config_file:
            config_dict = yaml.safe_load(config_file)
    else:
        config_dict = config

    return config_dict


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
    rllib_config["config"]["env"] = config["env"]["name"]

    return rllib_config


def get_default() -> dict:
    """Get default beobench config

    Returns:
        dict: default beobench config dict
    """

    config = {
        "agent": {
            "origin": "rllib",
            "config": {
                "run_or_experiment": "PPO",
                "stop": {"timesteps_total": 400000},
                "config": {
                    "lr": 0.005,
                    "model": {
                        "fcnet_activation": "relu",
                        "fcnet_hiddens": [256, 256, 256, 256],
                        "post_fcnet_activation": "tanh",
                    },
                    "batch_mode": "complete_episodes",
                    "gamma": 0.999,
                    "horizon": 1000,
                    "metrics_smoothing_episodes": 5,
                },
            },
        },
        "env": {
            "name": "MixedUseFanFCU-v0",
            "gym": "energym",
            "config": {
                "days": 365,
                "energym_environment": "MixedUseFanFCU-v0",
                "gym_kwargs": {
                    "max_episode_length": 35040,
                    "normalize": True,
                    "step_period": 15,
                },
                "weather": "GRC_A_Athens",
            },
        },
    }

    return config
