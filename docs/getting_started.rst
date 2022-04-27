Getting started
===============

.. include:: ./guides/installation.rst

Running a beobench experiment
-----------------------------

Most Beobench experiments start with an *experiment configuration*
in the form of either a yaml file or a Python dictionary. This
configuration fully defines the experiment, configuring everything
from the RL agent to the environment and its wrappers.

Let's look at a concrete example. Consider the ``config.yaml`` file below:


.. code-block:: yaml

  env:
    gym: sinergym
    config:
      name: Eplus-5Zone-hot-continuous-v1
      normalize: True
  agent:
    origin: ./agent.py
    config:
      num_steps: 100
  general:
    local_dir: ./beobench_results


Here, the first ``env`` part sets the environment to
``Eplus-5Zone-hot-continuous-v1``
from Sinergym. The ``env.config.normalize`` setting ensures
that the observations returned by the environment are normalized.

The ``general.local_dir`` setting determines that all data from
the experiment will be saved to the ``./beobench_results`` directory.

The ``agent`` part of the configuration sets the main code that is
executed inside the experiment container. Simply put, we can think of Beobench
as a way to (1) build a special Docker container and then (2) execute your code
(referred to as *agent script*) inside these containers. In this configuration
the ``agent.origin`` means that we use the local ``./agent.py`` script as our
agent script. This local script is executed
inside the container. Alternatively, there
are also a number of pre-defined agent scripts available, including
a script for
using RLlib.

Next, let's have look at an example ``agent.py`` script:

.. code-block:: python

  from beobench.experiment.provider import config, create_env

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
we import the ``config`` dictionary and the
``create_env`` function from ``beobench.experiment.provider``.
These two imports are only available inside an experiment container.
The ``config``
dictionary gives us access to the full experiment configuration
(as defined before). The ``create_env`` function allows us to create the environment
as definded in our configuration. Notably, we can use these two imports *regardless*
of the gym framework we are using. This invariability allows us to create
agent scripts that work across frameworks.

After the imports, the ``agent.py`` script sets up a loop that takes random
actions in the environment. Feel free to customize the agent script to your
requirements.

We can then run the experiment using the command

.. include:: ./snippets/run_standard_experiment.rst
