""" The experiment provider provides access to environments inside containers."""

import beobench.experiment.config_parser

try:
    import env_creator  # pylint: disable=import-outside-toplevel,import-error
except ImportError as e:
    raise ImportError(
        (
            "Cannot import env_creator module. Is Beobench being executed"
            "inside beobench experiment container?"
        )
    ) from e

config = beobench.experiment.config_parser.parse("/tmp/beobench/config.yaml")


def create_env(env_config: dict = None) -> object:
    """Create environment.

    Create environment from Beobench integration currently being used.
    This only works INSIDE a beobench experiment container.

    Args:
        env_config (dict, optional): env configuration. Defaults to None.

    Returns:
        object: environment instance
    """

    # Access env_creator script that is only available inside
    # experiment container.
    if env_config is None:
        env_config = config["env"]["config"]

    return env_creator.create_env(env_config)
