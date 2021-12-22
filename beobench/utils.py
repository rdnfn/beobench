"""Module with a number of utility functions."""


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


def merge_dicts(a: dict, b: dict, path: list = None, mutate_a: bool = False) -> dict:
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


    Raises:
        Exception: When dictionaries are inconsistent

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
                merge_dicts(a[key], b[key], path + [str(key)], mutate_a=True)
            elif a[key] == b[key]:
                pass  # same leaf value
            else:
                raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a