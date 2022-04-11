"""Energym-provided rule-based controller."""

from beobench.experiment.provider import config, create_env
import wandb
import numpy as np

import energym.examples.Controller  # import LabController

# Setting up experiment tracking via wandb
wandb_used = config["general"]["wandb_project"] is not None
if wandb_used:
    wandb.init(
        project=config["general"]["wandb_project"],
        entity=config["general"]["wandb_entity"],
        group=config["general"]["wandb_group"],
        name="energym_rbc_" + wandb.util.generate_id(),
    )

# Determining length of experiment (if set)
try:
    num_timesteps = config["agent"]["config"]["stop"]["timesteps_total"]
except KeyError:
    num_timesteps = 10

# Determine max length of an episode
try:
    horizon = config["agent"]["config"]["config"]["horizon"]
except KeyError:
    horizon = 1000


print("Energym rule-based controller agent: starting test.")

env = create_env()

inputs = env.env.get_inputs_names()
controller = energym.examples.Controller.LabController(
    control_list=inputs,
    lower_tol=0.3,
    upper_tol=0.8,
    nighttime_setback=True,
    nighttime_start=18,
    nighttime_end=6,
    nighttime_temp=18,
)

observation = env.reset()
outputs = env.env.get_output()

num_steps_per_ep = 0
episode = 0
ep_rewards = []
hour = 0

for _ in range(num_timesteps):
    episode += 1
    num_steps_per_ep += 1

    action = controller.get_control(outputs, 21, hour)
    action["Bd_Ch_EV1Bat_sp"] = [0.0]
    action["Bd_Ch_EV2Bat_sp"] = [0.0]

    # The steps below are based on the energym integration step() function
    # See https://github.com/rdnfn/beobench_contrib/blob/4c240bb/gyms/energym/energymGymEnv.py#L232

    # take step in energym environment
    outputs = env.env.step(action)
    # determine whether episode is finshed
    done = env.compute_done(outputs)
    # evaluate reward
    reward = env.compute_reward(outputs)

    ep_rewards.append(reward)

    if done or num_steps_per_ep >= horizon:

        if wandb_used:
            wandb.log({"episode_reward_mean": np.sum(ep_rewards), "step": episode})

        num_steps_per_ep = 0
        ep_rewards = []
        if done:
            observation = env.reset()
env.close()
print("Energym rule-based controller agent: completed test.")