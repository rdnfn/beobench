"""Module to test main run command."""

import pytest

import beobench

CMD_CONFIG = {
    "dev_path": ".",
    "force_build": True,
}


@pytest.mark.slow
def test_run_local(run_config):
    """Run beobench experiment using current state of beobench in
    experiment container."""
    beobench.run(config=run_config, **CMD_CONFIG)


@pytest.mark.skip(
    reason=(
        "This test may fail on breaking changes between versions,"
        " thus not running by default."
    )
)
@pytest.mark.slow
def test_run_pypi(run_config):
    """Run beobench experiment using latest pypi-beobench in experiment container."""
    beobench.run(config=run_config)


@pytest.mark.slow
def test_null_env_config():
    """Run beobench experiment using latest pypi-beobench in experiment container."""
    config = {
        "env": {"config": None},
        "agent": {"config": {"stop": {"timesteps_total": 10}}},
    }
    beobench.run(config=config, **CMD_CONFIG)


@pytest.mark.slow
def test_reqs_install(agent_sb3, requirements_sb3):
    config = {
        "agent": {
            "origin": str(agent_sb3),
            "requirements": str(requirements_sb3),
            "config": {"stop": {"timesteps_total": 10}},
        },
    }
    beobench.run(config=config, **CMD_CONFIG)
