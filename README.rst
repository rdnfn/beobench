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

A toolkit providing easy and unified access to building control reinforcement learning environments from multiple frameworks. Out of the box, Beobench provides access to environments from *BOPTEST*, *Energym*, and *Sinergym*. If required, Beobench can be easily extended to be used with other environments.

Features
--------
- **Largest collection of building control environments:** by combining the environments from *BOPTEST*, *Energym*, and *Sinergym*, Beobench is able to provide the (to the best of our knowledge) largest collection of building control environments (`see environment list here <https://beobench.readthedocs.io/en/latest/envs.html>`_).
- **Clean and light-weight installation:** Beobench is installed via pip and only requires Docker as an additional non-python dependency (`see installation guide <https://beobench.readthedocs.io/en/latest/guides/installation.html>`_). Other packages require the user to deal with building simulator installations or manage docker images directly.
- **Built-in RL agents:** Beobench allows the user to apply any agent from the `Ray RLlib collection <https://github.com/ray-project/ray/tree/master/rllib>`_ *in addition* to agents provided by the user directly.
- **Easily extendable:** want to use Beobench with an environment not yet included? The support for user-defined Docker contexts makes it easy to use Beobench with any RL environment.

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


.. _sec_envs:

Available environments
----------------------

.. csv-table::
        :header-rows: 1
        :widths: auto

        Gym,Environment,Type*,Description
        *BOPTEST*,``bestest_air``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/bestest_air/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/boptest.html>`_"
        ,``bestest_hydronic``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/bestest_hydronic/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/boptest.html>`_"
        ,``bestest_hydronic_heat_pump``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/bestest_hydronic_heat_pump/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/boptest.html>`_"
        ,``multizone_residential_hydronic``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/multizone_residential_hydronic/doc/MultiZoneResidentialHydronic.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/boptest.html>`_"
        ,``singlezone_commercial_hydronic``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://htmlpreview.github.io/?https://github.com/ibpsa/project1-boptest/blob/master/testcases/singlezone_commercial_hydronic/doc/index.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/boptest.html>`_"
        *Energym*,``Apartments2Thermal-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/ap2t.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``Apartments2Grid-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/ap2g.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``ApartmentsThermal-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/apt.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``ApartmentsGrid-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/apg.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``OfficesThermostat-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/offices.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``MixedUseFanFCU-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/mixeduse.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SeminarcenterThermostat-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/seminart.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SeminarcenterFull-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://bsl546.github.io/energym-pages/sources/seminarf.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SimpleHouseRad-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/houserad.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SimpleHouseRSla-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/houseslab.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SwissHouseRSlaW2W-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SwissHouseRSlaA2W-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SwissHouseRSlaTank-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss2.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        ,``SwissHouseRSlaTankDhw-v0``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://bsl546.github.io/energym-pages/sources/swiss2.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/energym.html>`_"
        *Sinergym*,``Eplus-demo-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-hot-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-mixed-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-cool-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-hot-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-mixed-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-cool-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-hot-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-mixed-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-cool-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-hot-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-mixed-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-5Zone-cool-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-datacenter-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-datacenter-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-datacenter-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-datacenter-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-IWMullion-discrete-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-IWMullion-continuous-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-IWMullion-discrete-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"
        ,``Eplus-IWMullion-continuous-stochastic-v1``,.. image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg,"`original <https://jajimer.github.io/sinergym/compilation/html/pages/environments.html>`_, `beobench <https://beobench.readthedocs.io/en/latest/envs/sinergym.html>`_"

\* Types of environments:

* residential |home|
* office |office|
* data center |industry|


License
-------
MIT license, see `credits and license page in docs <https://beobench.readthedocs.io/en/latest/credits.html>`_ for more detailed information.


