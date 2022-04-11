"""Module with various configuration constants"""

import pathlib

# read-only dir in container
CONTAINER_RO_DIR = pathlib.Path("/root/beobench_configs")

# output data dir in container
CONTAINER_DATA_DIR = pathlib.Path("/root/beobench_results")
RAY_LOCAL_DIR_IN_CONTAINER = CONTAINER_DATA_DIR / "ray_results"
