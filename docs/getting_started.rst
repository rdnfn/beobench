
.. _sec_quickstart:

Getting started
===============

.. tip::
  This section is (almost) identical to the quickstart section in the repository README. If you already read that one, you may want to skip to the :doc:`advanced usage guides<guides/index>`.

.. Note that below we import multiple separate parts from the main repo readme. This separation is done to allow us to add rst elements inbetween that can't be parsed by GitHubs rst parser.

.. include:: ../README.rst
   :start-after: start-qs-sec1
   :end-before: end-qs-sec1


.. admonition:: OS support

    - **Linux:** recommended and tested (Ubuntu 20.04).
    - **Windows:** use via `Windows Subsystem for Linux (WSL) <https://docs.microsoft.com/en-us/windows/wsl/install>`_ recommended.
    - **macOS:** experimental support for Apple silicon systems — only intended for development purposes (not running experiments). Intel-based macOS support untested.


.. include:: ../README.rst
   :start-after: start-qs-sec2
   :end-before: end-qs-sec2

.. note::

  We can use these two imports *regardless* of the gym framework we are using. This invariability allows us to create agent scripts that work across frameworks.

.. include:: ../README.rst
   :start-after: start-qs-sec3
   :end-before: end-qs-sec3


Given the configuration and agent script above, we can run the experiment using the command:

.. include:: ./snippets/run_standard_experiment.rst

.. include:: ../README.rst
   :start-after: start-qs-sec4
   :end-before: end-qs-sec4