"""Example agent script."""


import beobench.gym.core

env = beobench.gym.core.ContainerEnv(port=5672)

print(env.action_space)

env.reset()
for i in range(10):
    env.step(env.action_space.sample())
