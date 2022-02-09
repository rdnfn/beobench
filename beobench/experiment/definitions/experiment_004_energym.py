"""An experiment to test sinergym integration."""

import ray.tune
from beobench.experiment.definitions.default import problem, method, rllib_setup


problem = {
    "name": "sinergym_test_problem",
    "description": ("Control problem corresponding to " "created by sinergym env ''."),
    "problem_library": "https://github.com/rdnfn/beobench_contrib.git#dev/energym-integration:gyms/energym",
    "rllib_experiment_config": {
        "config": {
            "env": "MixedUseFanFCU-v0",
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
            # "output": "/root/ray_results/debug/",
            # "output_compress_columns": [],
            "batch_mode": "complete_episodes",
            "horizon": 1000,
            "metrics_smoothing_episodes": 5,
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
            "num_workers": 1,  # 1 for silent mode, can at least be 6
            "num_gpus": 1,
            "seed": ray.tune.randint(0, 10000000),
        },
        # "log_to_file": True,
        "checkpoint_freq": 10000,
    },
}
