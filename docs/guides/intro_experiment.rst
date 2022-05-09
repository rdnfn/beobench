Creating new experiments
------------------------

Overview
^^^^^^^^

The diagram below gives an overview of how beobench experiments work. The ``beobench.experiment.scheduler.run()`` function builds and starts an *experiment container*. Within this container all experiments are being run using the *Ray RLlib* and *Ray Tune* libraries. Results are saved to a local folder (by default ``./beobench_results``), and optionally to Weights and Biases (wandb) as well.

.. image:: ../_static/experiment_run_flow.png
   :width: 450 px
   :alt: experiment run diagram
   :align: center

Experiment configuration
^^^^^^^^^^^^^^^^^^^^^^^^^

Beobench experiments are configured either using a *Python dictionary* or an equivalent *yaml file*. For example, the following ``config.yaml`` file configures an experiment that evaluates an RLlib-based *proximal policy optimisation* (PPO) agent on the ``MixedUseFanFCU-v0`` environment of Energym:


.. literalinclude:: ../../beobench/data/configs/default.yaml
    :language: yaml



Given this configuration file ``config.yaml``, we can run the experiment using the following commands:

.. include:: ../snippets/run_standard_experiment.rst

Running experiment in background
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you're up and running with Beobench, you will likely eventually want to start running experiments in the background. One way of doing this on Linux is using ``nohup``:

.. code-block:: console

    nohup beobench run -c config.yaml &

This will save the console output of your experiment to `nohup.out` in your current directory.

If you have setup the Beobench development environment, you may want to start your experiments inside the devcontainer. You can do this using:

.. code-block:: console

    nohup docker exec <devcontainer_name> beobench run -c config.yaml &

