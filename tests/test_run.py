"""Module to test main run command."""

import pytest

import beobench
import beobench.experiment.config_parser


@pytest.fixture
def run_config():
    return beobench.experiment.config_parser.get_standard_config("simple")


@pytest.mark.slow
def test_run_command(run_config):
    beobench.run(config=run_config, dev_path=".[extended]")
