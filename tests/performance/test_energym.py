"""Tests to evaluate the performance of Beobench energym environments."""

import timeit
from datetime import datetime


def test_performance_on_fixed_actions(
    use_beobench: bool = False,
    config: dict = None,
    num_steps: int = 100,
    beobench_normalize: bool = False,
    beobench_use_native_env: bool = False,
):

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

        def take_steps():
            for _ in range(num_steps):
                env.step(action)

        step_time = timeit.timeit(take_steps, number=1)
        print("Performance test, step time (native): ", step_time)
        with open(
            "beobench_results/perf_test_results.txt", "a", encoding="utf-8"
        ) as text_file:
            text_file.write(
                (
                    f"  Performance, time for taking {num_steps}"
                    " in env: {step_time} seconds\n"
                )
            )

    else:
        import beobench  # pylint: disable=import-outside-toplevel

        if not beobench_use_native_env:
            # if beobench_normalize:
            action = {key: value[0] for key, value in action.items()}

        beobench_config = {
            "agent": {
                "origin": "../tests/performance/energym_fixed_action.py",
                "config": {
                    "action": action,
                    "num_steps": num_steps,
                    "use_native_env": beobench_use_native_env,
                },
            },
            "env": {
                "gym": "energym",
                "config": {
                    "energym_environment": config["env_name"],
                    "weather": config["weather"],
                    "days": config["simulation_days"],
                    "gym_kwargs": {
                        "normalize": beobench_normalize,
                    },
                },
            },
            "general": {
                "dev_path": "../",
                # "use_no_cache": True,
            },
        }
        beobench.run(config=beobench_config)


def main():
    """Main test function."""
    # pylint: disable=cell-var-from-loop

    NUM_STEPS = 10000  # pylint: disable=invalid-name
    for use_beobench, beobench_normalize, beobench_use_native_env in [
        (True, False, False),
        (True, True, False),
        (True, False, True),
        (False, None, None),
    ]:
        with open(
            "beobench_results/perf_test_results.txt", "a", encoding="utf-8"
        ) as text_file:
            text_file.write(str(datetime.now()) + "\n")
            text_file.write("New test - Configuration:\n")
            text_file.write(f"  use_beobench: {use_beobench}\n")
            text_file.write(f"  beobench_normalize: {beobench_normalize}\n")
            text_file.write(f"  beobench_use_native_env: {beobench_use_native_env}\n")
            text_file.write(f"  num_steps: {NUM_STEPS}\n\n")

        func_time = timeit.timeit(
            lambda: test_performance_on_fixed_actions(
                use_beobench=use_beobench,
                config=None,
                num_steps=NUM_STEPS,
                beobench_normalize=beobench_normalize,
                beobench_use_native_env=beobench_use_native_env,
            ),
            number=1,
        )
        with open(
            "beobench_results/perf_test_results.txt", "a", encoding="utf-8"
        ) as text_file:
            text_file.write(f"  Performance, overall time: {func_time} seconds\n\n")


if __name__ == "__main__":
    main()
