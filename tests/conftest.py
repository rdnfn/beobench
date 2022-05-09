"""Test configuration with fixtures."""

import pytest

import beobench.experiment.config_parser

collect_ignore_glob = ["performance"]


@pytest.fixture
def run_config():
    return beobench.experiment.config_parser.get_standard_config("simple")
