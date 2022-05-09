"""Random agent for testing beobench experiment containers"""

import wandb
import numpy as np

from beobench.experiment.provider import config, create_env

# Setting up experiment tracking via wandb
wandb_used = config["general"]["wandb_project"] is not None
if wandb_used:
    wandb.init(
        config={"beobench": config},
        project=config["general"]["wandb_project"],
        entity=config["general"]["wandb_entity"],
        group=config["general"]["wandb_group"],
        name="random_agent_" + wandb.util.generate_id(),
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


print("Random agent: starting test.")

env = create_env()
observation = env.reset()

num_steps_per_ep = 0
episode = 0
ep_rewards = []

infos = []
for _ in range(num_timesteps):
    episode += 1
    num_steps_per_ep += 1

    action = env.action_space.sample()
    observation, reward, done, info = env.step(action)

    infos.append(info)

    ep_rewards.append(reward)

    if done or num_steps_per_ep >= horizon:

        if wandb_used:
            wandb.log({"episode_reward_mean": np.sum(ep_rewards), "step": episode})

        num_steps_per_ep = 0
        ep_rewards = []
        if done:
            observation = env.reset()
env.close()

print("Random agent: completed test.")
