"""Module to test main run command."""

import pytest

import beobench


@pytest.mark.slow
def test_run_local(run_config):
    """Run beobench experiment using current state of beobench in
    experiment container."""
    beobench.run(config=run_config, dev_path=".")


@pytest.mark.slow
def test_run_pypi(run_config):
    """Run beobench experiment using latest pypi-beobench in experiment container."""
    beobench.run(config=run_config, force_build=True)


@pytest.mark.slow
def test_null_env_config():
    """Run beobench experiment using latest pypi-beobench in experiment container."""
    config = {"env": {"config": None}}
    beobench.run(config=config, force_build=True)
