"""Beobench gym API."""

from celery import Celery
from loguru import logger
import os

# Setup celery APP
celery_broker = os.environ.get("CELERY_BROKER")
inside_container = os.environ.get("INSIDE_BEOBENCH_CONTAINER")
if celery_broker is None:
    if inside_container is not None:
        from beobench.gym.env_access import create_env

        celery_broker = "pyamqp://guest@beobench-rabitmq-broker//"
        env = create_env()
        logger.info("Beobench.gym: initialised API inside container.")
    else:
        celery_broker = "pyamqp://guest@localhost:5672//"
        logger.info("Beobench.gym: initialised API locally.")
        env = None

# Everything below is important for the agent script too.
app = Celery(
    "remote-environment",
    broker=celery_broker,
    # This is important to let us wait for results, i.e. to  the
    # interaction with the environment synchronous.
    result_backend="rpc://",
    result_persistent=False,
    include=["beobench.gym.tasks"],
)
# Setting pickle allows API to send numpy arrays.
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]
