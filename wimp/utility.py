"""
"""

import distutils.sysconfig
import os
import pkgutil
import sys
from typing import Set


def gather_modules(path: str):
    """ """
    for mod in pkgutil.walk_packages([path]):
        yield mod
        if mod.ispkg:
            subpath = os.path.join(mod.module_finder.path, mod.name)
            for submod in gather_modules(subpath):
                yield submod


def get_stdlib() -> Set[str]:
    """Get a list of module names that (probably) comprises the Python standard
    library.
    """
    std = distutils.sysconfig.get_python_lib(standard_lib=True)
    stdlib = set(mod.name for mod in pkgutil.iter_modules([std]))
    stdlib.update(sys.builtin_module_names)
    return stdlib
