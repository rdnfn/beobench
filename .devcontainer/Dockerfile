# See here for image contents: https://github.com/microsoft/vscode-dev-containers/tree/v0.205.2/containers/python-3/.devcontainer/base.Dockerfile

# [Choice] Python version (use -bullseye variants on local arm64/Apple Silicon): 3, 3.10, 3.9, 3.8, 3.7, 3.6, 3-bullseye, 3.10-bullseye, 3.9-bullseye, 3.8-bullseye, 3.7-bullseye, 3.6-bullseye, 3-buster, 3.10-buster, 3.9-buster, 3.8-buster, 3.7-buster, 3.6-buster
ARG VARIANT="3.10"
FROM mcr.microsoft.com/vscode/devcontainers/python:0-${VARIANT}

# [Choice] Node.js version: none, lts/*, 16, 14, 12, 10
ARG NODE_VERSION="none"
RUN if [ "${NODE_VERSION}" != "none" ]; then su vscode -c "umask 0002 && . /usr/local/share/nvm/nvm.sh && nvm install ${NODE_VERSION} 2>&1"; fi

# [Optional] If your pip requirements rarely change, uncomment this section to add them to the image.
COPY requirements/requirements_dev.txt requirements/boptest_requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements_dev.txt \
    -r /tmp/pip-tmp/boptest_requirements.txt \
    && rm -rf /tmp/pip-tmp

# This enables that BOPTEST example files work. Note that this adds
# potentially some not so easily identifiable paths to the Python namespace.
# E.g. `examples`
ENV PYTHONPATH "${PYTHONPATH}:/opt/beobench/boptest:/opt/beobench/boptest_gym:/opt/beobench"
