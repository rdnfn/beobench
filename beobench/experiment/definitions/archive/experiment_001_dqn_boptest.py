"""Default experiment definitions."""

import ray.tune

import beobench.integrations.boptest
import beobench.utils
import beobench.experiment.definitions.default

problem = {
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
                "discretize": ray.tune.choice([4, 10, 20, 40]),
            },
            "gamma": 0.999,
        },
        "stop": {"timesteps_total": 400000},
    },
}

method = {
    "name": "DQN",
    "description": "Deep Q-network.",
    "rllib_experiment_config": {
        "run_or_experiment": "DQN",
        "config": {
            "lr": ray.tune.choice([0.001, 0.0001, 0.00001]),
            "model": {
                "fcnet_hiddens": [256, 256, 256, 256],
                "fcnet_activation": ray.tune.choice(["tanh", "linear", "relu"]),
                "post_fcnet_activation": ray.tune.choice(["tanh", "linear"]),
            },
        },
        "num_samples": 20,
    },
}

rllib_setup = beobench.experiment.definitions.default.rllib_setup
