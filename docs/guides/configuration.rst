YAML configuration
==================

Beobench uses `YAML files <https://en.wikipedia.org/wiki/YAML>`_ to define experiment configurations. The file below is the default configuration for every Beobench experiment. The comments above each setting describe its functionality.

.. literalinclude:: ../../beobench/data/configs/default.yaml
    :language: yaml


Gym-specific configurations
---------------------------

Each gym framework integration has its own configuration setup. See below for the default environment configurations of the three supported frameworks.

BOPTEST
^^^^^^^

.. literalinclude:: ../../beobench/data/configs/gym_boptest.yaml
    :language: yaml


Energym
^^^^^^^

.. literalinclude:: ../../beobench/data/configs/gym_energym.yaml
    :language: YAML

Sinergym
^^^^^^^^

.. literalinclude:: ../../beobench/data/configs/gym_sinergym.yaml
    :language: yaml