"""Random agent for testing beobench experiment containers"""

import beobench.experiment.provider

print("Random agent: creating env.")
env = beobench.experiment.provider.create_env()
print("Random agent: resetting env.")
observation = env.reset()
for _ in range(10):
    print("Random agent: taking action.")
    action = env.action_space.sample()
    print(action)
    observation, reward, done, info = env.step(action)
    if done:
        observation = env.reset()
env.close()
print("Random agent: completed test.")
