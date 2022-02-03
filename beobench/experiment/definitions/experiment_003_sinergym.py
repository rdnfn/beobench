"""An experiment to test sinergym integration."""

import ray.tune
from beobench.experiment.definitions.default import problem, method, rllib_setup


problem = {
    "name": "sinergym_test_problem",
    "description": ("Control problem corresponding to " "created by sinergym env ''."),
    "problem_library": "sinergym",
    "rllib_experiment_config": {
        "config": {
            "env": "sinergym-Eplus-5Zone-hot-continuous-v1",
            "env_config": {
                "name": "Eplus-5Zone-hot-continuous-v1",
                "normalize": True,
            },
            "gamma": 0.999,
            "output": "/root/ray_results/debug/",
            "output_compress_columns": [],
            "soft_horizon": False,
            "no_done_at_end": False,
            "horizon": 10000,
        },
        "stop": {"timesteps_total": 400000},
    },
}

rllib_setup = {
    "rllib_experiment_config": {
        "config": {
            # Utilities settings
            "framework": "torch",
            "log_level": "WARNING",
            "num_workers": 8,  # 1 for silent mode, can at least be 6
            "num_gpus": 1,
            "seed": ray.tune.randint(0, 10000000),
        },
        "log_to_file": True,
        "checkpoint_freq": 10000,
    },
}
