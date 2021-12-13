"""A collection of building energy optimisation problems."""


PROBLEM_001 = {
    "name": "problem_001",
    "description": (
        "Control problem corresponding to "
        " the BOPTEST testcase 'bestest_hydronic_heat_pump'."
    ),
    "problem_library": "boptest",
    "create_env_kwargs": {
        "gym_kwargs": {
            "actions": ["oveHeaPumY_u"],
            "observations": {"reaTZon_y": (280.0, 310.0)},
            "random_start_time": True,
            "max_episode_length": 86400,
            "warmup_period": 10,
            "step_period": 900,
        }
    },
}
