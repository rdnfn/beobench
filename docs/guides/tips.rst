Miscellaneous tips
------------------

Running experiment in background
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once you're up and running with Beobench, you will likely eventually want to start running experiments in the background. One way of doing this on Linux is using ``nohup``:

.. code-block:: console

    nohup beobench run -c config.yaml &

This will save the console output of your experiment to `nohup.out` in your current directory.

If you have setup the Beobench development environment, you may want to start your experiments inside the devcontainer. You can do this using:

.. code-block:: console

    nohup docker exec <devcontainer_name> beobench run -c config.yaml &

