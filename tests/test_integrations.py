"""Tests for Beobench integrations like Sinergym and Energym."""

import pytest
import beobench.experiment.config_parser
import beobench

CMD_CONFIG = {
    "dev_path": ".",
    "force_build": True,
}


@pytest.mark.slow
@pytest.mark.parametrize("gym_name", ["sinergym", "energym", "boptest"])
def test_gym(rand_agent_config, gym_name):
    """Run random agent beobench experiment with specified gym integration."""

    # get gym integration config and combine with random agent config
    env_config = beobench.experiment.config_parser.get_standard_config(
        f"gym_{gym_name}"
    )
    config = beobench.experiment.config_parser.parse([rand_agent_config, env_config])

    # limit num timesteps taken during test
    config["agent"]["config"]["stop"]["timesteps_total"] = 10

    # running actual experiment
    beobench.run(config=config, **CMD_CONFIG)
