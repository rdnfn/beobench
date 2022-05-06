"""Module to test main run command."""

import pytest

import beobench


@pytest.mark.slow
def test_run_command(run_config):
    beobench.run(config=run_config, dev_path=".")
