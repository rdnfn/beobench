Getting started
===============

.. _sec-installation:

Installation
------------

1. `Install docker <https://docs.docker.com/get-docker/>`_ on your machine (if on Linux, check the :doc:`additional installation steps <guides/installation_linux>`)
2. Install *beobench* using:

        .. code-block:: console

                pip install beobench


.. admonition:: OS support

        - **Linux:** recommended and tested (Ubuntu 20.04).
        - **Windows:** use via `Windows Subsystem for Linux (WSL) <https://docs.microsoft.com/en-us/windows/wsl/install>`_ recommended.
        - **macOS:** experimental support for Apple silicon systems --- only intended for development purposes (not running experiments). Intel-based macOS support untested.



Running a first experiment
--------------------------

Configuration
^^^^^^^^^^^^^



To get started with our first experiment, we set up an *experiment configuration*.
Experiment configurations
can be given as a yaml file or a Python dictionary. Such a configuration
fully defines an experiment, configuring everything
from the RL agent to the environment and its wrappers.

Let's look at a concrete example. Consider this ``config.yaml`` file:


.. code-block:: yaml

  agent:
    origin: ./agent.py
    config:
      num_steps: 100
  env:
    gym: sinergym
    config:
      name: Eplus-5Zone-hot-continuous-v1
      normalize: True
  general:
    local_dir: ./beobench_results

Here, the first ``agent`` part of the configuration determines what code is run inside the experiment container. Simply put, we can think of Beobench as a tool to (1) build a special Docker container and then (2) execute your code inside that container. The code run in step (2) is referred to as the *agent script*. In the ``config.yaml`` file above, this agent script is set to ``./agent.py`` via the ``agent.origin`` configuration.

Before looking more closely at an ``agent.py`` file, let us first consider the remaining configuration. The ``env`` part sets the environment to ``Eplus-5Zone-hot-continuous-v1`` from Sinergym. The ``env.config.normalize`` setting ensures that the observations returned by the environment are normalized. Finally, the ``general.local_dir`` setting determines that all data from the experiment will be saved to the ``./beobench_results`` directory.

Agent script
^^^^^^^^^^^^


Next, let's have look at an example *agent script*, ``agent.py``:

.. code-block:: python

  from beobench.experiment.provider import create_env, config

  # create environment and get starting observation
  env = create_env()
  observation = env.reset()

  for _ in range(config["agent"]["config"]["num_steps"]):
      # sample random action from environment's action space
      action = env.action_space.sample()
      # take selected action in environment
      observation, reward, done, info = env.step(action)

  env.close()

The most important part of this script is the first line:
we import the ``create_env`` function and the ``config`` dictionary from ``beobench.experiment.provider``.
These two imports are only available inside an experiment container. The ``create_env`` function allows us to create the environment
as definded in our configuration.
The ``config``
dictionary gives us access to the full experiment configuration
(as defined before).

.. note:: We can use these two imports *regardless* of the gym framework we are using. This invariability allows us to create agent scripts that work across frameworks.

After the imports, the ``agent.py`` script above sets up a loop that takes random
actions in the environment. Feel free to customize the agent script to your
requirements.

Alternatively, there
are also a number of pre-defined agent scripts available, including
a script for
using RLlib.

Execution
^^^^^^^^^

Given the configuration and agent script above, we can run the experiment using the command:

.. include:: ./snippets/run_standard_experiment.rst

This will command will:

1. Build an experiment container with Sinergym installed.
2. Execute ``agent.py`` inside that container.


.. toctree::
        :hidden:

        guides/installation_linux