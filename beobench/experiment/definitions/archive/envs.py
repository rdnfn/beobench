"""Definition of environments available in beobench."""

boptest_bestest_hydronic_heat_pump_v1 = {
    "name": "boptest_bestest_hydronic_heat_pump_v1",
    "description": (
        "Control problem corresponding to "
        "the BOPTEST testcase 'bestest_hydronic_heat_pump'."
    ),
    "problem_library": "boptest",
    "rllib_experiment_config": {
        "config": {
            "env": "boptest_bestest_hydronic_heat_pump_v1",
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

sinergym_eplus_5zone_hot_continous_v1 = {
    "name": "sinergym_eplus_5zone_hot_continous_v1",
    "description": "",
    "problem_library": "sinergym",
    "rllib_experiment_config": {
        "config": {
            "env": "sinergym_eplus_5zone_hot_continous_v1",
            "env_config": {
                "name": "Eplus-5Zone-hot-continuous-v1",
                "normalize": True,
            },
            "gamma": 0.999,
            "output": "/root/ray_results/debug/",
            "output_compress_columns": [],
            "batch_mode": "complete_episodes",
            "horizon": 1000,
            "metrics_smoothing_episodes": 5,
        },
        "stop": {"timesteps_total": 400000},
    },
}

energym_mixed_use_fan_fcu_v0 = {
    "name": "energym_mixed_use_fan_fcu_v0",
    "description": "",
    "problem_library": "energym",
    "rllib_experiment_config": {
        "config": {
            "env": "energym_mixed_use_fan_fcu_v0",
            "env_config": {
                "energym_environment": "MixedUseFanFCU-v0",
                "weather": "GRC_A_Athens",
                "days": 365,
                "gym_kwargs": {
                    "max_episode_length": 35040,
                    "step_period": 15,
                    "normalize": True,
                },
            },
            "gamma": 0.999,
            "output": "/root/ray_results/debug_energym/",
            "output_compress_columns": [],
            "batch_mode": "complete_episodes",
            "horizon": 1000,
            "metrics_smoothing_episodes": 5,
        },
        "stop": {"timesteps_total": 400000},
    },
}
