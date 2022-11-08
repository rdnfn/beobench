#!/usr/bin/env python3
"""
A simple dummy agent that will do steps of 1.
"""

import numpy as np

import gym

from envwrapper import step, reset

print("\nStarting local experiment.")
env = gym.make("CartPole-v0")
observation = env.reset()
print(f"Agent received initial observation: {observation} of type {type(observation)}")
for i in range(10):
    observation = env.step(np.array(1))
    print(f"Agent received observation: {observation} of type {type(observation)}")

print("\nStarting Celery experiment.")
async_result = reset.delay()
observation = async_result.get()
print(f"Agent received initial observation: {observation} of type {type(observation)}")

for i in range(10):
    try:
        async_result = step.delay(np.array(1))
        observation = async_result.get()
        print(f"Agent received observation: {observation} of type {type(observation)}")
        # sleep(1)
    except ConnectionError as e:
        print(f"Failed with exception {e}. Retrying.")
