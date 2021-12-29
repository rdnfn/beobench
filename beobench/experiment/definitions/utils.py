"""Utility functions for experiment definitions."""

import beobench.utils


def get_experiment_config(
    problem_def: dict, method_def: dict, rllib_setup_def: dict
) -> dict:
    """Combine partial ray tune experiment definitions into single definition.

    This recursively merges the dictionaries.

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

    Returns:
        dict: combined dictionary.
    """

    exp_config = {}

    exp_config = beobench.utils.merge_dicts(
        problem_def["rllib_experiment_config"], method_def["rllib_experiment_config"]
    )
    exp_config = beobench.utils.merge_dicts(
        exp_config, rllib_setup_def["rllib_experiment_config"]
    )

    exp_config["name"] = problem_def["name"] + "_" + method_def["name"]

    # Get combine the two dict into single experiment
    # conf file for ray.tune.run()
    return exp_config
