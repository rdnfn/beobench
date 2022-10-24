#!/usr/bin/env python3
"""
A simple dummy agent that will do steps of 1.
"""

from time import sleep

import numpy as np

from envwrapper import step, reset

async_result = reset.delay()
observation = async_result.get()
print(
    "Agent received initial observation: {} of type {}".format(
        observation, type(observation)
    )
)

while True:
    async_result = step.delay(np.ones(1))
    observation = async_result.get()
    print(
        "Agent received observation: {} of type {}".format(
            observation, type(observation)
        )
    )
    sleep(1)
