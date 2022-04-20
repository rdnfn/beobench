"""Module with various configuration constants"""

import pathlib

# available gym-framework integrations
AVAILABLE_INTEGRATIONS = [
    "boptest",
    "sinergym",
    "sinergym_minimal",
    "energym",
]

# available agent scripts
AVAILABLE_AGENTS = [
    "rllib",
    "random_action",
    "energym_controller",
]

AVAILABLE_WRAPPERS = [
    "general",
    "energym",
]

# read-only dir in container
CONTAINER_RO_DIR = pathlib.Path("/root/beobench_configs")

# output data dir in container
CONTAINER_DATA_DIR = pathlib.Path("/root/beobench_results")
RAY_LOCAL_DIR_IN_CONTAINER = CONTAINER_DATA_DIR / "ray_results"
