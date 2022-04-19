"""Environment wrappers that may be applied across gyms."""

import gym
import gym.spaces
import warnings
import wandb

from beobench.experiment.provider import config


class EnvResetCalledError(Exception):
    pass


class SubsetDictObs(gym.ObservationWrapper):
    """Wrapper that reduces dict observation space to subset."""

    def __init__(self, env, selected_obs_keys=None):
        """Wrapper that reduces dict observation space to subset.

        Args:
            env (_type_): _description_
            selected_obs_keys (_type_, optional): _description_. Defaults to None.
        """
        super().__init__(env)
        self.selected_obs_keys = selected_obs_keys
        self._observation_space = gym.spaces.Dict(
            {key: self.env.observation_space[key] for key in selected_obs_keys}
        )

    def observation(self, observation):
        return {key: observation[key] for key in self.selected_obs_keys}


class FixDictActs(gym.ActionWrapper):
    """Wrapper to fix some actions in dict action space."""

    def __init__(self, env: gym.Env, fixed_actions: dict = None):
        """Wrapper to fix some actions in dict action space.

        Args:
            env (gym.Env): environment to wrap.
            fixed_actions (dict, optional): dictionary of the values of fixed actions.
                Defaults to None.
        """
        super().__init__(env)
        self.fixed_actions = fixed_actions
        self._action_space = gym.spaces.Dict(
            {
                key: self.env.action_space[key]
                for key in self.env.action_space.keys()
                if key not in fixed_actions.keys()
            }
        )

    def action(self, action):
        return {**action, **self.fixed_actions}


class PreventReset(gym.Wrapper):
    """Wrapper to prevent more than one (initial) reset of the environment."""

    def __init__(self, env: gym.Env, raise_error: bool = False):
        """Wrapper to prevent more than one (initial) reset of the environment.

        Args:
            env (gym.Env): environment to wrap.
            raise_error (bool, optional): Whether to raise error. Defaults to False.
        """
        super().__init__(env)
        self.reset_raises_error = raise_error
        self.first_reset_done = False

    def reset(self, **kwargs):
        if self.first_reset_done is True:
            if self.reset_raises_error:
                raise EnvResetCalledError("Environment method .reset() called.")
            else:
                warnings.warn("Environment method .reset() called.")
                return self.env.reset(**kwargs)
        else:
            self.first_reset_done = True
            return self.env.reset(**kwargs)


class WandbLogger(gym.Wrapper):
    """Wrapper to log all env data for every xth step."""

    def __init__(self, env: gym.Env, log_freq: int = 1):
        """Wrapper to log all env data for every xth step.

        Args:
            env (gym.Env): environment to wrap.
            log_freq (int, optional): how often to log the step() method. E.g. for 2
                every second step is logged. Defaults to 1.
        """

        super().__init__(env)
        wandb.init(
            id=config["autogen"]["run_id"],
            project=config["general"]["wandb_project"],
            entity=config["general"]["wandb_entity"],
            group=config["general"]["wandb_group"],
        )
        self.log_freq = log_freq
        self.total_env_steps = 0

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        self.total_env_steps += 1

        if self.total_env_steps % self.log_freq == 0:
            log_dict = {
                "env": {
                    "action": action,
                    "obs": obs,
                    "reward": reward,
                    "done": done,
                    "info": info,
                    "step": self.total_env_steps,
                }
            }
            wandb.log(log_dict)

        return obs, reward, done, info
