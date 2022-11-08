#!/usr/bin/env python3
"""
This does the celery connection magic.
"""
from celery import Celery
import os

# This is a conditional import, i.e. it will import the environment if it is
# available (only in the environment container).
try:
    from environment.dummyenv import DummyEnvironment

    env = DummyEnvironment()

except ImportError:
    DummyEnvironment = None

try:
    os.environ["ENVCONTAINER"]  # pylint: disable=pointless-statement
    print("Using container broker.")
    broker = "pyamqp://guest@beobench-rabitmq-broker//"
except KeyError:
    print("Using localhost broker.")
    broker = "pyamqp://guest@localhost:5672//"


# Everything below is important for the agent script too.
app = Celery(
    "remote-environment",
    broker=broker,
    # This is important to let us wait for results, i.e. to  the
    # interaction with the environment synchronous.
    result_backend="rpc://",
    result_persistent=False,
)
# Allows to send numpy arrays.
app.conf.task_serializer = "pickle"
app.conf.result_serializer = "pickle"
app.conf.accept_content = ["application/json", "application/x-python-serialize"]


# Define the existing methods that can be called remotly to interact
@app.task
def reset():
    return env.reset()


@app.task
def step(action):
    return env.step(action)
