.. raw:: html

   <p align="center">

.. image:: ./docs/_static/beobench_logo.png
        :align: center
        :width: 300 px
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

A toolkit providing easy and unified access to building control reinforcement learning environments from multiple frameworks. Out of the box, Beobench provides access to environments from *BOPTEST*, *Energym*, and *Sinergym*. If required Beobench can be easily extended to be used with other environments.

Features
--------
- **Largest collection of building control environments:** by combining the environments from *BOPTEST*, *Energym*, and *Sinergym*, Beobench is able to provide the (to the best of our knowledge) largest collection of building control environments.
- **Clean and light-weight installation:** Beobench is installed via pip and only requires docker as an additional non-python dependency (:ref:`see quickstart <sec_quickstart>`). Other packages require the user to manage building simulation installations or deal directly with docker images.
- **Built-in RL agents:** Beobench allows the user to apply any agent from the `Ray RLlib collection <https://github.com/ray-project/ray/tree/master/rllib>`_ *in addition* to agents provided by the user directly.
- **Easily extendable:** want to use Beobench to evaluate RL agents on an environment not yet included in Beobench? The use of docker contexts makes it easy to use Beobench with any RL environment.



Available environments
----------------------

.. csv-table::
        :header-rows: 1
        :widths: auto

        Gym,Environment,Type
        *BOPTEST*,bestest_air,🏠
        ,bestest_hydronic,🏠
        ,bestest_hydronic_heat_pump,🏠
        ,multizone_residential_hydronic,🏠
        ,singlezone_commercial_hydronic,🏢
        *Energym*,Apartments2Thermal-v0,🏠
        ,Apartments2Grid-v0,🏠
        ,ApartmentsThermal-v0,🏠
        ,ApartmentsGrid-v0,🏠
        ,OfficesThermostat-v0,🏢
        ,MixedUseFanFCU-v0,🏢
        ,SeminarcenterThermostat-v0,🏢
        ,SeminarcenterFull-v0,🏢
        ,SimpleHouseRad-v0,🏠
        ,SimpleHouseRSla-v0,🏠
        ,SwissHouseRSlaW2W-v0,🏠
        ,SwissHouseRSlaA2W-v0,🏠
        ,SwissHouseRSlaTank-v0,🏠
        ,SwissHouseRSlaTankDhw-v0,🏠
        *Sinergym*,Eplus-demo-v1,🏠
        ,Eplus-5Zone-hot-discrete-v1,🏠
        ,Eplus-5Zone-mixed-discrete-v1,🏠
        ,Eplus-5Zone-cool-discrete-v1,🏠
        ,Eplus-5Zone-hot-continuous-v1,🏠
        ,Eplus-5Zone-mixed-continuous-v1,🏠
        ,Eplus-5Zone-cool-continuous-v1,🏠
        ,Eplus-5Zone-hot-discrete-stochastic-v1,🏠
        ,Eplus-5Zone-mixed-discrete-stochastic-v1,🏠
        ,Eplus-5Zone-cool-discrete-stochastic-v1,🏠
        ,Eplus-5Zone-hot-continuous-stochastic-v1,🏠
        ,Eplus-5Zone-mixed-continuous-stochastic-v1,🏠
        ,Eplus-5Zone-cool-continuous-stochastic-v1,🏠
        ,Eplus-datacenter-discrete-v1,🏭
        ,Eplus-datacenter-continuous-v1,🏭
        ,Eplus-datacenter-discrete-stochastic-v1,🏭
        ,Eplus-datacenter-continuous-stochastic-v1,🏭
        ,Eplus-IWMullion-discrete-v1,🏢
        ,Eplus-IWMullion-continuous-v1,🏢
        ,Eplus-IWMullion-discrete-stochastic-v1,🏢
        ,Eplus-IWMullion-continuous-stochastic-v1,🏢



Features
--------

*Some of the features are work in progress*

Main features

- *RL algorithm collection:* what's the best RL method for your BEO problem? Building on `Ray RLlib <https://github.com/ray-project/ray/tree/master/rllib>`_, beobench provides a large collection of pre-configured RL algorithm experiments that can be easily applied to your new BEO problem.
- *Problem collection:* beobench provides ready-to-use docker containers for popular BEO gym-type problem libraries. By enforcing a strict OpenAI ``gym.Env`` it makes testing your method on different libraries easy.

Additional features

- *Experiment logging:* log experiment results in a reproducible and shareable manner via `Weights and Biases`_.
- *Hyperparameter tuning:* easily tune hyperparameters using the extensive `Ray Tune Search API <https://docs.ray.io/en/master/tune/index.html>`_.
- *Simple installation:* beobench can be installed via pip and only requires docker as an additional non-python dependency.
- *Easily extendable:* beobench is designed for the user to add both environments and methods.

.. _Weights and Biases: https://wandb.ai/

.. end-in-sphinx-docs


.. start-quickstart
.. _sec_quickstart:

Quickstart
----------

Run your first beobench experiment in three steps:

1. `Install docker <https://docs.docker.com/get-docker/>`_ on your machine (if on Linux, check the `additional installation steps <https://beobench.readthedocs.io/en/latest/guides/installation_linux.html>`_)
2. Install *beobench* using:

        .. code-block:: console

                pip install beobench

3. Finally, start your first experiment using:

        .. code-block:: console

                beobench run

Done, you have just started your first experiment... congrats! Check out the `full getting started guide in the documentation <https://beobench.readthedocs.io/en/latest/guides/getting_started.html>`_ for the next steps.

.. end-quickstart

Documentation
-------------
https://beobench.readthedocs.io

License
-------
MIT license



Credits
-------

This package was originally created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
