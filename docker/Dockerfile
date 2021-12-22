# Beobench main docker file
# To build this use
# > docker build -t beobench:latest -f ./docker/Dockerfile .

FROM python:3.7

# Beobench setup below (copied from dev container)
COPY requirements/requirements_dev.txt requirements/boptest_requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements_dev.txt \
    -r /tmp/pip-tmp/boptest_requirements.txt \
    && rm -rf /tmp/pip-tmp

# Install beobench problem set libraries
# TODO: replace this with pip installation instead of
# python path manipulation
ENV MAIN_PYTHONPATH = "${PYTHONPATH}"
ENV PYTHONPATH "${PYTHONPATH}:/tmp"
COPY beobench/installer.py beobench/constants.py /tmp/beobench/
RUN python /tmp/beobench/installer.py \
    && rm -rf /tmp/beobench
ENV PYTHONPATH = "${MAIN_PYTHONPATH}"
