""" """

import os
import pkgutil
import sys


def gather_modules(path: str):
    """ """
    for mod in pkgutil.walk_packages([path]):
        yield mod
        if mod.ispkg:
            subpath = os.path.join(mod.module_finder.path, mod.name)
            for submod in gather_modules(subpath):
                yield submod


def get_stdlib() -> set[str]:
    """Get a list of module names that (probably) comprises the Python standard
    library.
    """
    return set(sys.builtin_module_names) | sys.stdlib_module_names
