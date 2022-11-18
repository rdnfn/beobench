"""Module with a number of utility functions."""

import docker
import subprocess

import beobench.logging
from beobench.logging import logger


def check_if_in_notebook() -> bool:
    """Check if code is executed from jupyter notebook.

    Taken from https://stackoverflow.com/a/44100805.

    Returns:
        bool: whether code is run from notebook.
    """
    try:
        # This function should only be available in ipython kernel.
        get_ipython()  # pylint: disable=undefined-variable
        return True
    except:  # pylint: disable=bare-except
        return False


def merge_dicts(
    a: dict,
    b: dict,
    path: list = None,
    mutate_a: bool = False,
    let_b_overrule_a=False,
) -> dict:
    """Merge dictionary b into dictionary a.

    Adapted from https://stackoverflow.com/a/7205107.

    Args:
        a (dict): a dicitonary
        b (dict): another dictionary
        path (list, optional): where the dict is in the original dict.
            Necessary for recursion, no need to use. Defaults to None.
        mutate_a (bool, optional): whether to mutate the dictionary a that
            is given. Necessary for recursion, no need to use.
            Defaults to False.
        let_b_overrule_a: whether to allow dict b to overrule if they disagree on a
            key value. Defaults to False.


    Raises:
        Exception: When dictionaries are inconsistent, and not let_b_overrule_a.

    Returns:
        dictionary: merged dictionary.
    """
    # pylint: disable=consider-using-f-string

    # Ensure that dict a is not mutated
    if not mutate_a:
        a = dict(a)

    if path is None:
        path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge_dicts(
                    a[key],
                    b[key],
                    path + [str(key)],
                    mutate_a=True,
                    let_b_overrule_a=let_b_overrule_a,
                )
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                if not let_b_overrule_a:
                    location = ".".join(path + [str(key)])
                    raise Exception(
                        (
                            f"Conflict at {location}."
                            f"a={a[key]} is not the same as b={b[key]}."
                        )
                    )
                else:
                    a[key] = b[key]
        else:
            a[key] = b[key]
    return a


def shutdown() -> None:
    """Shut down all beobench and BOPTEST containers."""

    beobench.logging.setup()

    logger.info("Stopping any remaining beobench and BOPTEST docker containers...")

    client = docker.from_env()
    container_num = 0
    for container in client.containers.list():
        if "auto_beobench" in container.name or "auto_boptest" in container.name:
            logger.info(f"Stopping container {container.name}")
            container.stop(timeout=0)
            container_num += 1

    logger.info(f"Stopped {container_num} container(s).")


def restart() -> None:
    """Clean up remaining beobench processes and containers
    before running new experiments.

    This stops all docker containers still running. This
    function is not called by other scheduler functions
    to enable the parallel running of experiments.
    """

    shutdown()


def run_command(cmd_line_args, process_name):
    """Run command and log its output."""

    process = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd_line_args,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    with process.stdout:
        beobench.logging.log_subprocess(
            process.stdout,
            process_name=process_name,
        )
    retcode = process.wait()  # 0 means success
    if retcode:
        raise subprocess.CalledProcessError(retcode, cmd=cmd_line_args)
