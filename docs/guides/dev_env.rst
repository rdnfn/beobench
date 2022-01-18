.. highlight:: shell

Setting up development environment
-----------------------

Requirements
^^^^^^^^^^^^^^^^^^

Beobench uses `vscode dev containers <https://code.visualstudio.com/docs/remote/containers-tutorial>`_ for its development environment. The installation has the following pre-requisites on the local machine:

1. `Docker <https://docs.docker.com/get-docker/>`_
2. `Visual Studio Code (vscode) <https://code.visualstudio.com/>`_
3. `vscode remote extension pack <https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.vscode-remote-extensionpack>`_

Additionally, for remote development, the remote machine must have docker installed.


Local development
^^^^^^^^^^^^^^^^^^


1. Clone the repo locally to your machine using

   .. code-block::

        git clone git@github.com:rdnfn/beobench.git

2. Open the git repo folder in vscode
3. Inside vscode, open the command palette (shortcut is ``shift`` + ``cmd`` + ``P`` on macos), and use the ``Remote-containers: open folder in container`` command. Select the ``beobench`` repo in the pop-up window (NOT the ``beobench`` folder inside the repo).

This should have opened a new vscode window running in the docker dev container -- once the dev container is ready you're done! (Note: this gets faster after the first docker build)


Remote development
^^^^^^^^^^^^^^^^^^

It may be desireable to run your dev container on a remote machine. In order to do this you need to follow the following steps:

1. Follow all the instructions for local development above (apart from the final step 3).
2. Clone the repo to your *remote* machine.
3. In the cloned repo on your local machine, in ``.devcontainer/devcontainer.json`` replace the line

   .. code-block::

        "workspaceMount": "source=/home/rdnfn-docker/main/repos/github/beobench/,target=/workspace,type=bind,consistency=cached"


   with

   .. code-block::

        "workspaceMount": "source=<PATH_TO_CLONED_REPO>,target=/workspace,type=bind,consistency=cached"

   where ``PATH_TO_CLONED_REPO`` is the path to your repo on the remote machine.

4. Create a docker context on your local machine that connects to docker on your remote machine (`See the instructions here <https://stackoverflow.com/a/63814363>`_).
5. Use the ``Remote-containers: open folder in container`` command and select the ``beobench`` repo in the pop-up window (NOT the ``beobench`` folder inside the repo).

