"""Experiment config parser module"""

from typing import Union
import pathlib
import yaml


def parse(config: Union[str, pathlib.Path]) -> dict:
    """Parse experiment config from yaml file to dict.

    Args:
        config (Union[str, pathlib.Path]): path of yaml file
    """

    # load config dict if path given
    if isinstance(config, (str, pathlib.Path)):
        # make sure config is a real path
        if isinstance(config, str):
            config = pathlib.Path(config)
        with open(config) as config_file:
            config_dict = yaml.safe_load(config_file)
    else:
        config_dict = config

    return config_dict
