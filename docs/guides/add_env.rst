Adding your own environment
-----------------------------

This guide explains how to add a new reinforcement learning (RL) environment to beobench.

.. admonition:: Why should I use this?

    Adding your RL environment to beobench allows you to test all of RLlib's methods on your environment without actually implementing any methods yourself. It also allows you to compare the performance of agents across your and other beobench environments, enabling you to compare your environment's difficulty.


Creating build context
^^^^^^^^^^^^^^^^^^^^^^^^^^^

To add an environment to beobench we need to create a special *docker build context* (for more details `see the official docker build documentation <https://docs.docker.com/engine/reference/commandline/build/>`_). Such a beobench-specific *docker build context* consists at least of the following two files in a folder ``<your_gym_name>/``:

1. A dockerfile ``Dockerfile`` that defines a docker container that has everything necessary for your environment installed. In addition to any of your packages/modules, the dockerfile must also install `beobench` via pip.
2. An ``env_creator.py`` file that defines a function with the signature ``create_env(env_config: dict = None) -> gym.Env``. This ``create_env()`` function should take an ``env_config`` dictionary (that completely configures your environment) as input and return an instance of your environment with this configuration. If your environment is not yet implementing the commonly used ``gym.Env`` class (`see here <https://github.com/openai/gym/blob/e9df4932434516c9f7956cc8010679a33835b204/gym/core.py#L17>`_), you will need to wrap your environment in a class that implements this ``gym.Env`` class within the ``create_env()`` function.

The path to the folder with these two files, ``path/to/folder/<your_gym_name>/``, can either be on your local file system or on github. It can also contain additional files that help with the installation process.

**Example**: for an example of such a *docker context folder* see `the official BOPTEST integration folder <https://github.com/rdnfn/beobench_contrib/tree/main/gyms/boptest>`_.


Defining experiment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order run an experiment on your gym, we need to add the build context to an experiment definition. This can be done by adding/changing the following parameter in your experiment definition file ``config.yaml`` (see :doc:`/guides/intro_experiment` for how to create a complete experiment definition file):

.. code-block:: yaml

    # ...
    env:
        gym: "path/to/folder/<your_gym_name>/"
    # ...


For example, we could set the ``gym`` key to ``"https://github.com/rdnfn/beobench_contrib.git#main:gyms/boptest"``.

.. warning::

    Only set ``gym`` to experiment build contexts from authors that you trust. This setting can create an arbitrary docker container on your system.

Running experiment
^^^^^^^^^^^^^^^^^^^^^^^^^^^

With a complete experiment definition file ``config.yaml``, we can then use the standard command below to start the experiment:

.. include:: ../snippets/run_standard_experiment.rst

Done! You have now successfully integrated your RL environment with beobench.