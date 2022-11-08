"""Test of celery step perf overhead."""

import timeit

NUM_SAMPLES = 1000

time_local = timeit.timeit(
    "env.step(np.array(1))",
    setup='import gym\nimport numpy as np\nenv = gym.make("CartPole-v0")\nenv.reset()',
    number=NUM_SAMPLES,
)

time_celery = timeit.timeit(
    "async_result = step.delay(np.array(1))\nobservation = async_result.get()",
    setup=(
        "from envwrapper import step, reset\n"
        "import numpy as np\nasync_result = reset.delay()\n"
        "observation = async_result.get()"
    ),
    number=NUM_SAMPLES,
)

print(
    (
        f"Timeit results: {time_local/NUM_SAMPLES:0.6f}s (local) "
        f"vs {time_celery/NUM_SAMPLES:0.6f}s (celery)"
    )
)
