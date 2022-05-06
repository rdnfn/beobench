"""Simple fixed action agent for time testing."""

from beobench.experiment.provider import config, create_env
from beobench.constants import CONTAINER_DATA_DIR
import timeit

env = create_env()

action = config["agent"]["config"]["action"]
num_steps = config["agent"]["config"]["num_steps"]
use_native_env = config["agent"]["config"]["use_native_env"]

print("Beobench: fixed actions being taken.")

if use_native_env:

    def take_steps():
        for _ in range(num_steps):
            env.env.step(action)

else:

    def take_steps():
        for _ in range(num_steps):
            env.step(action)


step_time = timeit.timeit(take_steps, number=1)
with open(
    CONTAINER_DATA_DIR / "perf_test_results.txt", "a", encoding="utf-8"
) as text_file:
    text_file.write(
        f"  Performance, time for taking {num_steps} in env: {step_time} seconds\n"
    )
print("Performance test, step time (beobench): ", step_time)

print("Beobench: fixed action test completed.")

env.close()
