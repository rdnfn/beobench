.. raw:: html

   <p align="center">

.. image:: ./docs/_static/beobench_logo.png
        :align: center
        :width: 300 px
        :alt: Beobench

.. raw:: html

   </p>


.. image:: https://img.shields.io/pypi/v/beobench.svg
        :target: https://pypi.python.org/pypi/beobench

.. image:: https://img.shields.io/travis/rdnfn/beobench.svg
        :target: https://travis-ci.com/rdnfn/beobench

.. image:: https://readthedocs.org/projects/beobench/badge/?version=latest
        :target: https://beobench.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status

A toolbox for benchmarking reinforcement learning (RL) algorithms on building energy optimisation (BEO) problems. Beobench does not replace existing libraries defining BEO problems (such as `BOPTEST <https://github.com/ibpsa/project1-boptest>`_) — instead it makes working with them easier.

Features
--------

- *Wide range of RL algorithms:* test the most common RL algorithms on BEO problems without re-implementing by using beobench's `Ray RLlib <https://github.com/ray-project/ray/tree/master/rllib>`_ integration.
- *Experiment logging:* log experiment results in a reproducible and sharable manner via `Weights and Biases`_.
- *Hyperparameter tuning:* easily tune hyperparameters using the extensive `Ray Tune syntax <https://docs.ray.io/en/master/tune/index.html>`_.
- *Installers:* avoid having to manage messy Python namespaces yourself — just install beobench via pip and use its pre-configured docker containers to take care of managing other BEO packages and their dependencies.

.. _Weights and Biases: https://wandb.ai/

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
