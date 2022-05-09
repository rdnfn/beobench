"""RLlib integration in beobench."""

import json
import ray.tune
import ray.tune.integration.wandb
import ray.tune.integration.mlflow

import beobench.utils
import beobench.experiment.config_parser
import beobench.integration.wandb
from beobench.constants import RAY_LOCAL_DIR_IN_CONTAINER


def run_in_tune(
    config: dict,
) -> ray.tune.ExperimentAnalysis:
    """Run beobench experiment.

    Additional info: note that RLlib is a submodule of the ray package, i.e. it is
    imported as `ray.rllib`. For experiment definitions it uses the `ray.tune`
    submodule. Therefore ray tune experiment definition means the same as ray rllib
    experiment defintions. To avoid confusion all variable/argument names use rllib
    instead of ray tune but strictly speaking these are ray tune experiment
    definitions.

    Args:
        config (dict): beobench config
        wandb_project (str, optional): name of wandb project. Defaults to None.
        wandb_entity (str, optional): name of wandb entirty. Defaults to None.
        mlflow_name (str, optional): name of mlflow experiment. Defaults to None.
        use_gpu (bool, optional): whether to use GPU. Defaults to False.

    Raises:
        ValueError: raised if only one of wandb project or wandb entity given.

    Returns:
        ray.tune.ExperimentAnalysis: analysis object from experiment.
    """

    if config["general"]["wandb_project"] and config["general"]["wandb_entity"]:

        callbacks = [
            ray.tune.integration.wandb.WandbLoggerCallback(
                project=config["general"]["wandb_project"],
                entity=config["general"]["wandb_entity"],
                group=config["general"]["wandb_group"],
                id=config["autogen"]["run_id"],
                config={"beobench": config},
            )
        ]
    elif config["general"]["wandb_project"] or config["general"]["wandb_entity"]:
        raise ValueError(
            "Only one of wandb_project or wandb_entity given, but both required."
        )
    elif config["general"]["mlflow_name"]:
        callbacks = [_create_mlflow_callback(config["general"]["mlflow_name"])]
    else:
        callbacks = []

    # combine the three incomplete ray tune experiment
    # definitions into a single complete one.
    rllib_config = beobench.experiment.config_parser.create_rllib_config(config)

    # change RLlib setup if GPU used
    if config["general"]["use_gpu"]:
        rllib_config["config"]["num_gpus"] = 1

    # register the problem environment with ray tune
    # provider is a module available in experiment containers
    # pylint: disable=import-outside-toplevel,import-error
    from beobench.experiment.provider import create_env

    ray.tune.registry.register_env(
        rllib_config["config"]["env"],
        create_env,
    )

    # if run in notebook, change the output reported throughout experiment.
    if beobench.utils.check_if_in_notebook():
        reporter = ray.tune.JupyterNotebookReporter(overwrite=True)
    else:
        reporter = None

    # running the experiment
    analysis = ray.tune.run(
        progress_reporter=reporter,
        callbacks=callbacks,
        local_dir=RAY_LOCAL_DIR_IN_CONTAINER,
        **rllib_config,
    )

    return analysis


def _create_mlflow_callback(
    mlflow_name: str,
):
    """Create an RLlib MLflow callback.

    Args:
        mlflow_name (str, optional): name of MLflow experiment.

    Returns:
        : a wandb callback
    """
    mlflow_callback = ray.tune.integration.mlflow.MLflowLoggerCallback(
        experiment_name=mlflow_name, tracking_uri="file:/root/ray_results/mlflow"
    )
    return mlflow_callback


def get_cross_episodes_data(path: str) -> dict:
    """Get concatenated episode data from RLlib output.

    This currently only concatenates data from info variable.
    It further assumes that each info returned by step() in the env is
    a dict of dicts.

    Args:
        path (str): path to RLlib output json file.

    Returns:
        dict: dictionary with episode data
    """
    # TODO: add non-info data to this logging procedure

    # Open RLlib output
    outputs = []
    with open(path, encoding="UTF-8") as json_file:
        for line in json_file.readlines():
            outputs.append(json.loads(line))

    # Get all keys of observations saved in info dict
    all_obs_keys = []
    for info_key in outputs[0]["infos"][0].keys():
        all_obs_keys += list(outputs[0]["infos"][0][info_key].keys())

    # Create empty (flat) dict of obs saved in info dict
    infos = []

    # Add data to dict, one step at a time
    for output in outputs[:]:
        for info in output["infos"]:
            infos.append(info)

    return infos
