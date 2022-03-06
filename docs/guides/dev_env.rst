.. highlight:: shell

Setting up development environment
-----------------------

Requirements
^^^^^^^^^^^^^^^^^^

Beobench uses `vscode devcontainers <https://code.visualstudio.com/docs/remote/containers-tutorial>`_ for its development environment. A devcontainer allows all developers to work on (almost) identical systems, ensuring that not only python packages but also operating systems are the same. The installation of this development environment has the following pre-requisites:

1. `Docker <https://docs.docker.com/get-docker/>`_
2. `Visual Studio Code (vscode) <https://code.visualstudio.com/>`_
3. `vscode remote extension pack <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack>`_


Standard development
^^^^^^^^^^^^^^^^^^^^

1. Fork the Beobench repo on GitHub (if you are a maintainer you can skip this step).
2. Clone your fork locally using

     .. code-block::

        git clone --recursive git@github.com:your_name_here/beobench.git

   (if you are a maintainer you can clone directly from the main repository)

   Note that this requires having your github authentification setup, `see here <https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account>`_

3. Open the beobench repo folder in vscode
4. Inside vscode, open the command palette (e.g. on macOS shortcut is ``shift`` + ``cmd`` + ``P``), and use the ``Remote-containers: reopen in container`` command.

This should have opened a new vscode window running in the docker dev container --- once the dev container is ready you're done! (Note: this gets faster after the first docker build)


Remote development
^^^^^^^^^^^^^^^^^^

.. note::
     Remote development is only useful if you have a separate server available to develop on. The standard development in the previous section will be more useful in most scenarios.


It may be desireable to run your devcontainer not directly on your local machine (e.g. laptop) but instead on a remote machine (i.e. server). The local machine then just provides an interface to the remote machine.

In order to set this up you need to follow these steps:

1. Follow all the instructions for local development above (apart from the final step 4).
2. Ensure that docker is installed on the remote machine.
3. Clone the repo to your *remote* machine.
4. In the cloned repo on your local machine, in ``.devcontainer/remote/.devcontainer/devcontainer.json`` replace the line

   .. code-block::

        "workspaceMount": "source=/home/rdnfn-docker/main/repos/github/beobench/,target=/workspace,type=bind,consistency=cached"


   with

   .. code-block::

        "workspaceMount": "source=<PATH_TO_CLONED_REPO>,target=/workspace,type=bind,consistency=cached"

   where ``PATH_TO_CLONED_REPO`` is the path to your repo on the remote machine. Similarly, adapt the path in the ``"mounts"`` argument to the location of your ``.gitconfig`` file on the remote machine.

5. Create a docker context on your local machine that connects to docker on your remote machine (`See the instructions here <https://stackoverflow.com/a/63814363>`_).
6. Use the ``Remote-containers: open folder in container`` command and select the ``beobench/.devcontainer/remote`` folder in the pop-up window (beobench here is the main repo folder).

