"""Environment wrappers for energym environments."""

import gym


class CustomReward(gym.Wrapper):
    """Wrapper to customize reward of energym environments."""

    def __init__(self, env: gym.Env, info_obs_weights: dict):
        """Wrapper to customize reward of energym environments.

        Args:
            env (gym.Env): environment to be wrapped.
            info_obs_weights (dict): dictionary with keys matching the info[obs] values
                to be combined as a linear combination with the weights given. E.g.
                {'power_ev':0.4, 'power_hvac':0.6} will make the env.step() method
                return a negative reward signal computed by

                ```
                info['obs']['power_ev'] * 0.4 + info['obs']['power_hvac'] * 0.6
                ```
        """
        super().__init__(env)
        self.info_obs_weights = info_obs_weights

    def step(self, action):
        obs, _, done, info = self.env.step(action)

        reward = sum(  # pylint: disable=consider-using-generator
            [info["obs"][key] * value for key, value in self.info_obs_weights.items()]
        )
        return obs, reward, done, info
