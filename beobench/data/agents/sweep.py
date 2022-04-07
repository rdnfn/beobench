"""Script to run wandb sweeps via Beobench."""

import wandb
import beobench
import beobench.experiment.provider
import beobench.experiment.config_parser
import beobench.utils

# Get the base config of experiment
base_config = beobench.experiment.provider.config["agent"]["config"]["base_config"]
base_config = beobench.experiment.config_parser.parse(base_config)


def sweep_func():

    wandb.init(dir="/root/ray_results/")
    print("initialised wandb inside sweep func.")

    # loading config params from sweep and combining them with base config
    tmp_config = dict(wandb.config)
    print("Config given by wandb", tmp_config)
    tmp_config = beobench.utils.merge_dicts(
        a=base_config,
        b=tmp_config,
        let_b_overrule_a=True,
    )
    print("Config given by sweep:", tmp_config)
    beobench.run(
        config=tmp_config,
        no_additional_container=True,
    )


# Setting up sweep config
sweep_config = beobench.experiment.provider.config["agent"]["config"]["sweep_config"]
sweep_config["program"] = "beobench"

# Starting sweep
sweep_id = wandb.sweep(sweep_config)

# Creating agent (for sweep)
wandb.agent(sweep_id, function=sweep_func)
