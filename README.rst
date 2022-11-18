.. raw:: html

   <p align="center">

.. image:: https://github.com/rdnfn/beobench/raw/0c520a7acd992fef2901c0b576fb948e061e2e1a/docs/_static/beobench_logo_v2_large.png
        :align: center
        :width: 400 px
        :alt: Beobench

.. raw:: html

   </p>

.. start-in-sphinx-docs

.. image:: https://img.shields.io/pypi/v/beobench.svg
        :target: https://pypi.python.org/pypi/beobench

.. image:: https://readthedocs.org/projects/beobench/badge/?version=latest
        :target: https://beobench.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

.. image:: https://img.shields.io/badge/License-MIT-blue.svg
        :target: https://opensource.org/licenses/MIT
        :alt: License

A toolkit providing easy and unified access to building control environments for reinforcement learning (RL). Compared to other domains, `RL environments for building control <https://github.com/rdnfn/rl-building-control#environments>`_ tend to be more difficult to install and handle. Most environments require the user to either manually install a building simulator (e.g. `EnergyPlus <https://github.com/NREL/EnergyPlus>`_) or to manually manage Docker containers. This can be tedious.

Beobench was created to make building control environments easier to use and experiments more reproducible. Beobench uses Docker to manage all environment dependencies in the background so that the user doesn't have to. A standardised API, illustrated in the figure below, allows the user to easily configure experiments and evaluate new RL agents on building control environments.

.. raw:: html

   <p align="center">

.. image:: https://github.com/rdnfn/beobench/raw/0c520a7acd992fef2901c0b576fb948e061e2e1a/docs/_static/beobench_architecture_horizontal_v1.png
        :align: center
        :width: 550 px
        :alt: Beobench

.. raw:: html

   </p>


Features
========

- **Large collection of building control environments:** Out-of-the-box Beobench provides access to environments from `BOPTEST <https://github.com/ibpsa/project1-boptest>`_, `Energym <https://github.com/bsl546/energym>`_, and `Sinergym <https://github.com/jajimer/sinergym>`_. Beobench combines the environments from these frameworks into the *(to the best of our knowledge)* largest single collection of building control environments. `See environment list here <https://beobench.readthedocs.io/en/latest/envs.html>`_.
- **Clean and light-weight installation:** Beobench is installed via pip and only requires Docker as an additional non-python dependency (`see installation guide <https://beobench.readthedocs.io/en/latest/guides/installation.html>`_). Without Beobench, most building control environments will require manually installing building simulators or directly managing docker containers.
- **Built-in RL agents:** Beobench allows the user to apply any agent from the `Ray RLlib collection <https://github.com/ray-project/ray/tree/master/rllib>`_ *in addition* to agents provided by the user directly.
- **Easily extendable:** want to use Beobench with an environment not yet included? The support for user-defined Docker contexts makes it easy to use Beobench with any RL environment.

.. end-in-sphinx-docs


.. _sec_quickstart:

Quickstart
==========

.. start-qs-sec1

.. _sec_installation:

Installation
------------

1. `Install docker <https://docs.docker.com/get-docker/>`_ on your machine (if on Linux, check the `additional installation steps <https://beobench.readthedocs.io/en/latest/guides/installation_linux.html>`_)
2. Install Beobench using:

        .. code-block:: console

                pip install beobench


.. end-qs-sec1

..

        **Warning**: **OS support**

        - **Linux:** recommended and tested (Ubuntu 20.04).
        - **Windows:** only use via `Windows Subsystem for Linux (WSL) <https://docs.microsoft.com/en-us/windows/wsl/install>`_ recommended.
        - **macOS:** experimental support for Apple silicon systems — only intended for development purposes (not running experiments). Intel-based macOS support untested.

.. start-qs-sec2

Running a first experiment
--------------------------

Experiment configuration
^^^^^^^^^^^^^^^^^^^^^^^^

To get started with our first experiment, we set up an *experiment configuration*.
Experiment configurations
can be given as a yaml file or a Python dictionary. The configuration
fully defines an experiment, configuring everything
from the RL agent to the environment and its wrappers. The figure below illustrates the config structure.

.. raw:: html

   <p align="center">

.. image:: https://github.com/rdnfn/beobench/raw/2cf961a8135b25c9a66e70d67eea9890ce0b878a/docs/_static/beobench_config_v1.png
        :align: center
        :width: 350 px
        :alt: Beobench

.. raw:: html

   </p>


Let's look at a concrete example. Consider this ``config.yaml`` file:


.. code-block:: yaml

  agent:
    # script to run inside experiment container
    origin: ./agent.py
    # configuration that can be accessed by script above
    config:
      num_steps: 100
  env:
    # gym framework from which we want use an environment
    gym: sinergym
    # gym-specific environment configuration
    config:
      # sinergym environment name
      name: Eplus-5Zone-hot-continuous-v1
  wrappers: [] # no wrappers added for this example
  general:
    # save experiment data to ``./beobench_results`` directory
    local_dir: ./beobench_results


Agent script
^^^^^^^^^^^^

The ``agent.origin`` setting in the configuration file above sets the *agent script* to be ``./agent.py``. The *agent script* is the main code that is run inside the experiment container. Most of the time this script will define an RL agent but it could really be anything. Simply put, we can think of Beobench as a tool to (1) build a special Docker container and then (2) execute an *agent script* inside that container.

Let's create an example *agent script*, ``agent.py``:

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

The only Beobench-specific part of this script is the first line:
we import the ``create_env`` function and the ``config`` dictionary from ``beobench.experiment.provider``.
The ``create_env`` function allows us to create the environment
as definded in our configuration.
The ``config``
dictionary gives us access to the full experiment configuration
(as defined before). These two imports are only available inside an experiment container.

.. end-qs-sec2

..

        **Note**

        We can use these two imports *regardless* of the gym framework we are using. This invariability allows us to create agent scripts that work across frameworks.

.. start-qs-sec3

After these Beobench imports, the ``agent.py`` script above just takes a few random actions in the environment. Feel free to customize the agent script to your requirements.

Alternatively, there are also a number of pre-defined agent scripts available, including a script for using RLlib.

Execution
^^^^^^^^^

.. end-qs-sec3

Given the configuration and agent script above, we can run the experiment either via the command line:

.. code-block:: console

        beobench run --config config.yaml

or in Python:

.. code-block:: python

        import beobench

        beobench.run(config = "config.yaml")

.. start-qs-sec4

Either command will:

1. Build an experiment container with Sinergym installed.
2. Execute ``agent.py`` inside that container.

You have just run your first Beobench experiment.


Next steps
^^^^^^^^^^

To learn more about using Beobench, look at the `advanced usage section <https://beobench.readthedocs.io/en/latest/advanced_usage.html>`_ in the documentation.

.. end-qs-sec4

Documentation
=============
https://beobench.readthedocs.io


.. _sec_envs:

Available environments
======================

.. csv-table::
        :header-rows: 1
        :widths: auto

        Gym,Environment,Type*,Description
        *BOPTEST*,``bestest_air``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/bestest_air/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id1>`_"
        ,``bestest_hydronic``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/bestest_hydronic/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id1>`_"
        ,``bestest_hydronic_heat_pump``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/bestest_hydronic_heat_pump/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id1>`_"
        ,``multizone_residential_hydronic``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/multizone_residential_hydronic/doc/MultiZoneResidentialHydronic.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id1>`_"
        ,``singlezone_commercial_hydronic``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/singlezone_commercial_hydronic/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id1>`_"
        *Energym*,``Apartments2Thermal-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/ap2t.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``Apartments2Grid-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/ap2g.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``ApartmentsThermal-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/apt.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``ApartmentsGrid-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/apg.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``OfficesThermostat-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/offices.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``MixedUseFanFCU-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/mixeduse.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SeminarcenterThermostat-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/seminart.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SeminarcenterFull-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/seminarf.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SimpleHouseRad-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/houserad.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SimpleHouseRSla-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/houseslab.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SwissHouseRSlaW2W-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SwissHouseRSlaA2W-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SwissHouseRSlaTank-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss2.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        ,``SwissHouseRSlaTankDhw-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss2.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id7>`_"
        *Sinergym*,``Eplus-demo-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-hot-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-mixed-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-cool-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-hot-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-mixed-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-cool-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-hot-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-mixed-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-cool-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-hot-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-mixed-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-5Zone-cool-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-datacenter-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-datacenter-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-datacenter-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-datacenter-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-IWMullion-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-IWMullion-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-IWMullion-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"
        ,``Eplus-IWMullion-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs.html#id25>`_"

\* Types of environments:

* residential |home|
* office |office|
* data center |industry|

.. |office| image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg
.. |home| image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg
.. |industry| image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg


Support
=======

Need help using Beobench or want to discuss the toolkit? Reach out via ``contact-gh (at) arduin.io`` and we are very happy to help either via email or in a call.


Citation
========

If you find Beobench helpful in your work, please consider citing the `accompanying paper <https://dl.acm.org/doi/10.1145/3538637.3538866>`_:

.. code-block::

        @inproceedings{10.1145/3538637.3538866,
        author = {Findeis, Arduin and Kazhamiaka, Fiodar and Jeen, Scott and Keshav, Srinivasan},
        title = {Beobench: A Toolkit for Unified Access to Building Simulations for Reinforcement Learning},
        year = {2022},
        isbn = {9781450393973},
        publisher = {Association for Computing Machinery},
        address = {New York, NY, USA},
        url = {https://doi.org/10.1145/3538637.3538866},
        doi = {10.1145/3538637.3538866},
        booktitle = {Proceedings of the Thirteenth ACM International Conference on Future Energy Systems},
        pages = {374–382},
        numpages = {9},
        keywords = {reinforcement learning, building energy optimisation, building simulation, building control},
        location = {Virtual Event},
        series = {e-Energy '22}
        }

License
=======
MIT license, see `credits and license page in docs <https://beobench.readthedocs.io/en/latest/credits.html>`_ for more detailed information.


