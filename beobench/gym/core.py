"""Core script with Environment based that accesses other env via script."""

import gym
from gym.core import ActType, ObsType
from typing import Tuple, Optional
import beobench.gym.celery
import beobench.gym.tasks
from beobench.gym.tasks import call_task


class ContainerEnv(gym.Env):
    """Environment connected via Celery to Docker container."""

    def __init__(self, port: int = 5672) -> None:
        """Environment connected via Celery to Docker container."""

        beobench.gym.celery.app.conf.broker_url = f"pyamqp://guest@localhost:{port}//"
        attributes = [
            "action_space",
            "observation_space",
            "reward_range",
            "spec",
            "metadata",
            "np_random",
        ]
        for attr_name in attributes:
            setattr(
                self,
                attr_name,
                call_task(beobench.gym.tasks.get_env_attr, {"name": attr_name}),
            )
        super().__init__()

    def step(self, action: ActType) -> Tuple[ObsType, float, bool, bool, dict]:
        return call_task(beobench.gym.tasks.step, {"action": action})

    def reset(
        self, *, seed: Optional[int] = None, options: Optional[dict] = None
    ) -> Tuple[ObsType, dict]:
        return call_task(beobench.gym.tasks.reset, {"seed": seed, "options": options})
