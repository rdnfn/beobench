"""A collection of building energy optimisation problems."""

import ray.tune

import beobench.integrations.boptest
import beobench.utils

PROBLEM_001_BOPTEST_HEATPUMP = {
    "name": "problem_001",
    "description": (
        "Control problem corresponding to "
        "the BOPTEST testcase 'bestest_hydronic_heat_pump'."
    ),
    "env_creator_to_register": beobench.integrations.boptest.create_env,
    "rllib_experiment_config": {
        "config": {
            "env": "beobench.integrations.boptest.create_env",
            "env_config": {
                "boptest_testcase": "bestest_hydronic_heat_pump",
                "gym_kwargs": {
                    "actions": ["oveHeaPumY_u"],
                    "observations": {"reaTZon_y": (280.0, 310.0)},
                    "random_start_time": True,
                    "max_episode_length": 86400,
                    "warmup_period": 10,
                    "step_period": 900,
                },
                "normalize": True,
            },
            "gamma": 0.999,
        },
        "stop": {"training_iteration": 50},
    },
}

METHOD_001_PPO = {
    "name": "PPO",
    "description": "Proximal policy optimisation.",
    "rllib_experiment_config": {
        "run_or_experiment": "PPO",
        "config": {
            "lr": 5e-3,
            "model": {
                "fcnet_hiddens": [256, 256, 256, 256],
                "fcnet_activation": "relu",
                "post_fcnet_activation": "tanh",
            },
        },
    },
}

RLLIB_SETUP = {
    "rllib_experiment_config": {
        "config": {
            # Utilities settings
            "framework": "torch",
            "log_level": "WARNING",
            "num_workers": 6,  # 1 for silent mode, can at least be 6
            "num_gpus": 0,
            "seed": ray.tune.randint(0, 10000000),
        },
        "local_dir": "./tmp/tune/",
        "log_to_file": True,
        "checkpoint_freq": 10000,
        "num_samples": 5,
    },
}


def get_experiment_config(
    problem_def: dict, method_def: dict, rllib_setup: dict
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
        exp_config, rllib_setup["rllib_experiment_config"]
    )

    exp_config["name"] = problem_def["name"] + "_" + method_def["name"]

    # Get combine the two dict into single experiment
    # conf file for ray.tune.run()
    return exp_config
