"""Test configuration with fixtures."""

import pytest

import beobench.experiment.config_parser

collect_ignore_glob = ["performance"]

AGENT_SB3 = """
import stable_baselines3
"""

REQUIREMENTS_SB3 = """
stable-baselines3[extra]
"""


def create_tmp_file(folder, name, content, factory):
    file_path = factory.mktemp(folder) / name
    file_path.write_text(content)
    return file_path


@pytest.fixture
def run_config():
    return beobench.experiment.config_parser.get_standard_config("test_energym")


@pytest.fixture
def rand_agent_config():
    return beobench.experiment.config_parser.get_standard_config("method_random_action")


@pytest.fixture(scope="session")
def agent_sb3(tmp_path_factory):
    agent_file_path = create_tmp_file(
        "agent_tmp", "agent.py", AGENT_SB3, tmp_path_factory
    )
    return agent_file_path


@pytest.fixture(scope="session")
def requirements_sb3(tmp_path_factory):
    agent_file_path = create_tmp_file(
        "requirements_tmp", "requirements.txt", REQUIREMENTS_SB3, tmp_path_factory
    )
    return agent_file_path
