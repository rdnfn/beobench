"""Tests to evaluate the performance of energym environments in Beobench."""


def test_performance_of_10k_actions(use_beobench: bool = False, config: dict = None):

    if config is None:
        config = {
            "env_name": "MixedUseFanFCU-v0",
            "weather": "GRC_A_Athens",
            "simulation_days": 300,
        }

    action = {
        "Bd_Fl_AHU1_sp": [1],
        "Bd_Fl_AHU2_sp": [1],
        "Bd_T_AHU1_sp": [21],
        "Bd_T_AHU2_sp": [21],
        "Z02_T_Thermostat_sp": [21],
        "Z03_T_Thermostat_sp": [21],
        "Z04_T_Thermostat_sp": [21],
        "Z05_T_Thermostat_sp": [21],
        "Z08_T_Thermostat_sp": [21],
        "Z09_T_Thermostat_sp": [21],
        "Z10_T_Thermostat_sp": [21],
        "Z11_T_Thermostat_sp": [21],
    }

    if not use_beobench:

        import energym  # pylint: disable=import-outside-toplevel

        env = energym.make(
            config["env_name"],
            weather=config["weather"],
            simulation_days=config["simulation_days"],
        )

        for _ in range(100):
            env.step(action)

    else:

        import beobench

        config = {"agent": ""}


if __name__ == "__main__":
    test_performance_of_10k_actions(use_beobench=False, config=None)
