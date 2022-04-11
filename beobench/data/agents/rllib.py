"""RLlib agent."""

import beobench.integration.rllib
from beobench.experiment.provider import config

beobench.integration.rllib.run_in_tune(config)
