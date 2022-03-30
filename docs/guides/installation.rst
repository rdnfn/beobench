.. highlight:: shell




.. _sec-installation:

Installation
------------------

Recommended method
^^^^^^^^^^^^^^^^^^

1. `Install docker <https://docs.docker.com/get-docker/>`_ on your machine (if on Linux, check the :doc:`additional installation steps <installation_linux>`)
2. Install *beobench* using:

        .. code-block:: console

                pip install beobench

Look at the :doc:`getting started guide <getting_started>` to run your first beobench experiment.

.. admonition:: OS support

        Beobench is recommended to be used on Linux systems. There is experimental support for ``aarch64``/``arm64``-based macOS systems (M1 Macs). Note that this uses ``amd64``-based docker containers, leading to limited performance – it is therefore only intended for development purposes (not running experiments). On Windows systems it is recommended to use Windows Subsystem for Linux (WSL) to run Beobench.

Directly from GitHub
^^^^^^^^^^^^^^^^^^^^

If you would like to get the truly latest (but not necessarily stable) version of beobench, you can replace the `pip install` command above with the following command:

.. code-block:: console

        pip install git+https://github.com/rdnfn/beobench

This will install the latest version directly from the master branch on GitHub.


Development environment
^^^^^^^^^^^^^^^^^^^^^^^

If you would like to contribute to beobench, use :doc:`this guide <dev_env>` to set up the full development environment.