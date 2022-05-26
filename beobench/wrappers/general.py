"""Environment wrappers that may be applied across gyms."""

import gym
import gym.spaces
import warnings
import wandb
import numpy as np

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

    def __init__(
        self,
        env: gym.Env,
        log_freq: int = 1,
        summary_metric_keys: list = None,
        restart_sum_metrics_at_reset: bool = False,
    ):
        """Wrapper to log all env data for every xth step.

        Args:
            env (gym.Env): environment to wrap.
            log_freq (int, optional): how often to log the step() method. E.g. for 2
                every second step is logged. Defaults to 1.
            summary_metric_keys (list, optional): list of keys of logged metrics for
                summary metrics such as cummulative sum and mean are computed. This
                defaults to ["env.returns.reward"]. WARNING: summary metrics only
                work for log_feq == 1, otherwise the cummulative metrics will not be
                correct.
        """

        if summary_metric_keys is None:
            summary_metric_keys = ["env.returns.reward"]

        super().__init__(env)
        wandb.init(
            id=config["autogen"]["run_id"],
            project=config["general"]["wandb_project"],
            entity=config["general"]["wandb_entity"],
            group=config["general"]["wandb_group"],
        )
        self.log_freq = log_freq
        self.total_env_steps = 0
        self.restart_sum_metrics_at_reset = restart_sum_metrics_at_reset
        self.cum_metrics = {key: 0 for key in summary_metric_keys}
        self.num_env_resets = 0
        self.last_log_dict = {}

    def step(self, action):
        obs, reward, done, info = self.env.step(action)

        self.total_env_steps += 1

        if self.total_env_steps % self.log_freq == 0:
            # TODO: enable flat dict for dict action and observation spaces
            # This would allow for summary values of invididual actions/observations
            if isinstance(action, (list, np.ndarray)):
                for i, act in enumerate(action):
                    new_action = {f"{i}": act}
                action = new_action

            log_dict = {
                "env.inputs.action": action,
                "env.returns.obs": obs,
                "env.returns.reward": reward,
                "env.returns.done": done,
                "env.total_steps": self.total_env_steps,
                **{f"env.returns.info.{key}": value for key, value in info.items()},
            }
            log_dict = self._create_summary_metrics(log_dict)
            wandb.log(log_dict)
            self.last_log_dict = log_dict

        return obs, reward, done, info

    def reset(self):

        if self.restart_sum_metrics_at_reset:
            wandb.log({"reset": self.last_log_dict, "reset.num": self.num_env_resets})
            self.cum_metrics = {key: 0 for key in self.cum_metrics.keys()}
            self.num_env_resets += 1

        return self.env.reset()

    def _create_summary_metrics(self, log_dict: dict):
        """Create summary of variables in log dict.

        In particular, the

        Args:
            log_dict (dict): _description_

        Returns:
            _type_: _description_
        """

        for key in self.cum_metrics.keys():
            self.cum_metrics[key] += log_dict[key]
            log_dict[key + "_cum"] = self.cum_metrics[key]
            log_dict[key + "_mean"] = self.cum_metrics[key] / self.total_env_steps

        return log_dict
