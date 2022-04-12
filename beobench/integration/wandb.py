"""Module with tools for using Beobench with wandb."""

import wandb


def log_eps_data(eps_dict: dict) -> None:
    """Log episode data to wandb.

    To be used with concatenated episode data from get_cross_episodes_data().

    Args:
        eps_dict (dict): episode data
    """

    eps_dict_len = len(list(eps_dict.values())[0])
    for i in range(eps_dict_len):
        single_eps_dict = {key: values[i] for key, values in eps_dict.items()}
        wandb.log({"env_step": i, **single_eps_dict})
