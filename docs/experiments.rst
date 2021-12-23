===========
Experiments
===========

How to run experiments

Create dev container with vscode

Then outside of dev container, start dev container::

    docker start <dev_container_name>

And then::

    nohup docker exec <dev_container_name> python -m beobench.experiment.scheduler --use-wandb --wandb-api-key=<your_api_key> &