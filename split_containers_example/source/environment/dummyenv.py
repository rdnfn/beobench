#!/usr/bin/env python3
"""
Some placeholder for a propper gym environment.
"""
import numpy as np


class DummyEnvironment:
    """
    Replace this with a proper gym environemt.
    """

    internal_state = None

    def reset(self):
        self.internal_state = np.zeros(1)
        observation = self.internal_state
        print("RESET. Obs is: {}".format(observation))
        return observation

    def step(self, action):
        self.internal_state += action
        observation = self.internal_state
        print("STEP. Obs is: {}".format(observation))
        return observation
