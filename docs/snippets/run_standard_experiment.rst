.. tabs::

    .. code-tab:: console Console

            python -m beobench.experiment.scheduler \
                --experiment-file example_experiment_def.py

    .. code-tab:: python

        import beobench.experiment.scheduler

        beobench.experiment.scheduler.run(
            experiment_file = "example_experiment_def.py",
        )