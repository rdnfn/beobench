"""Default experiment definitions."""

import ray.tune

import beobench.integrations.boptest

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
        "stop": {"timesteps_total": 400000},
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
            "num_workers": 8,  # 1 for silent mode, can at least be 6
            "num_gpus": 1,
            "seed": ray.tune.randint(0, 10000000),
        },
        "local_dir": "./tmp/tune/",
        "log_to_file": True,
        "checkpoint_freq": 10000,
    },
}


problem = PROBLEM_001_BOPTEST_HEATPUMP
method = METHOD_001_PPO
rllib_setup = RLLIB_SETUP
