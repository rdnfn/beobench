"""Beobench methods based on RLlib."""

# Proximal policy optimisation
# https://docs.ray.io/en/latest/rllib-algorithms.html#proximal-policy-optimization-ppo
PPO = {
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
