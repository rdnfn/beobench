"""Celery tasks.

Structure based on
https://docs.celeryq.dev/en/stable/getting-started/next-steps.html"""

from beobench.gym.celery import app, env

# Define the existing methods that can be called remotely to interact
@app.task
def reset(seed, options):
    return env.reset(seed=seed, options=options)


@app.task
def step(action):
    return env.step(action)


@app.task
def get_env_attr(name: str):
    return getattr(env, name)


def call_task(task: callable, kwargs: dict):
    async_result = task.delay(**kwargs)
    return async_result.get()
