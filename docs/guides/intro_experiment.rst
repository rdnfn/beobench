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

Beobench experiments are configured either using a *Python dictionary* or an equivalent *yaml file*. For example, the following ``example.yaml`` file configures an experiment that evaluates an RLlib-based *proximal policy optimisation* (PPO) agent on the ``MixedUseFanFCU-v0`` environment of Energym:


.. literalinclude:: ../../beobench/experiment/definitions/default.yaml
    :language: yaml



Given this configuration file ``example.yaml``, we can run the experiment using the following commands:

.. include:: ../snippets/run_standard_experiment.rst

