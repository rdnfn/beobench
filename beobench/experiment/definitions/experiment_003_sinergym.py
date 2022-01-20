"""An experiment to test sinergym integration."""

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
        },
        "stop": {"timesteps_total": 400000},
    },
}
