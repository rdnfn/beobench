#!/usr/bin/env python3
"""
A simple dummy agent that will do steps of 1.
"""

from time import sleep

import numpy as np

from envwrapper import step, reset

async_result = reset.delay()
observation = async_result.get()
print(f"Agent received initial observation: {observation} of type {type(observation)}")

for i in range(1000):
    try:
        async_result = step.delay(np.ones(1))
        observation = async_result.get()
        print(f"Agent received observation: {observation} of type {type(observation)}")
        sleep(1)
    except ConnectionError as e:
        print(f"Failed with exception {e}. Retrying.")
