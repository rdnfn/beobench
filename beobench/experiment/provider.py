""" The experiment provider provides access to environments inside containers."""

import beobench.experiment.config_parser
import importlib
from beobench.constants import CONTAINER_RO_DIR, AVAILABLE_WRAPPERS

try:
    import env_creator  # pylint: disable=import-outside-toplevel,import-error
except ImportError as e:
    raise ImportError(
        (
            "Cannot import env_creator module. Is Beobench being executed"
            "inside a Beobench experiment container?"
        )
    ) from e

config = beobench.experiment.config_parser.parse(CONTAINER_RO_DIR / "config.yaml")


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

    env = env_creator.create_env(env_config)

    for wrapper_dict in config["wrappers"]:
        wrapper = _get_wrapper(wrapper_dict)
        if "config" in wrapper_dict.keys():
            wrapper_config = wrapper_dict["config"]
        else:
            wrapper_config = {}
        env = wrapper(env, **wrapper_config)

    return env


def _get_wrapper(wrapper_dict):
    origin = wrapper_dict["origin"]

    if origin in AVAILABLE_WRAPPERS:
        wrapper_module_str = "beobench.wrappers." + origin
        wrapper_module = importlib.import_module(wrapper_module_str)
        wrapper_class = getattr(wrapper_module, wrapper_dict["class"])
        return wrapper_class
    else:
        raise NotImplementedError("Non-standard wrappers are currently not supported.")
