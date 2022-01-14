Quickstart
----------

Let's run your first experiment with beobench. After installing beobench using the :ref:`installation guide <sec-installation>`, you can simply use one of the following two commands to run a first experiment:

.. tabs::

    .. code-tab:: console Console

            python -m beobench.experiment.scheduler

    .. code-tab:: python

        import beobench.experiment.scheduler

        beobench.experiment.scheduler.run()

This will run the default experiment `defined here <beobench/experiment/definitions/default.py>`_: Proximal Policy Optimisation (PPO) applied a testcase in the BOPTEST library.