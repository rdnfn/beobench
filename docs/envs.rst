============
Environments
============

Beobench provides easy access to a large number of building control environments for reinforcement learning. Each environment comes from one of the integrated frameworks `BOPTEST <https://github.com/ibpsa/project1-boptest>`_, `Energym <https://github.com/bsl546/energym>`_ and `Sinergym <https://github.com/jajimer/sinergym>`_. The list below shows links to all environments available out-of-the-box. Each environment is marked based on whether it represents a residential building (|home|), office (|office|) or data center (|industry|).

.. include:: envs/envs_list.rst


.. |office| image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-skyscraper.svg
.. |home| image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/home.svg
.. |industry| image:: https://raw.githubusercontent.com/tabler/tabler-icons/master/icons/building-factory.svg

----

BOPTEST
-------

.. include:: ../beobench_contrib/gyms/boptest/README.md
    :parser: myst_parser.sphinx_
    :start-line: 2

.. include:: envs/BOPTEST_descriptions.rst


----

Energym
-------

.. include:: ../beobench_contrib/gyms/energym/README.md
    :parser: myst_parser.sphinx_
    :start-line: 2

.. include:: envs/Energym_descriptions.rst

----

Sinergym
--------

.. include:: ../beobench_contrib/gyms/sinergym/README.md
    :parser: myst_parser.sphinx_
    :start-line: 2

.. include:: envs/Sinergym_descriptions.rst