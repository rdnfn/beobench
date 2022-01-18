Additional installation steps on Linux
-----------------------------------------

Docker behaves differently depending on your OS. In Linux, many docker commands require additional privileges that can be granted by adding ``sudo`` in front of the command. Beobench relies on docker for most of its functionality. Therefore, there are two options to get beobench to work on a Linux system:

1. Always use ``sudo`` in front of beobench commands to grant the relevant privileges required for docker (note that this has not been tested)
2. *Recommended:* follow the official post-installation steps to `manage docker as a non-root user <https://docs.docker.com/engine/install/linux-postinstall/#manage-docker-as-a-non-root-user>`_ to enable running docker without ``sudo``. As the linked documentation points out, this carries a certain security risk.