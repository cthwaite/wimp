"""Summarise Python imports in a given context.
"""

import argparse
import ast
import distutils.sysconfig
import json
import os
import pkgutil
import sys
from typing import Any, Dict, Generator, List, Optional, Set

_TRANSLATE = {
    "pkg_resources": "setuptools",
}


def iter_code_cells(cells: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Iterate over cells in a Jupyter notebook, yielding source code from code cells."""
    for cell in cells:
        if cell["cell_type"] == "code":
            yield "".join(cell["source"])


class ImportCollector(ast.NodeVisitor):
    def __init__(self, ignore: Optional[List[str]] = None):
        super().__init__()
        self.imports = set()
        self.ignore = set(ignore) if ignore else set()

    def _push_name(self, name: str):
        if name not in self.ignore:
            self.imports.add(_TRANSLATE.get(name, name))

    def visit_Import(self, node: ast.Import):
        for alias in node.names:
            name, *_ = alias.name.split(".")
            self._push_name(name)

    def visit_ImportFrom(self, node: ast.ImportFrom):
        if node.module is not None:
            name = node.module
            if "." in name:
                name, *_ = name.split(".")
            if node.level == 0:
                self._push_name(name)


def gather_modules(path: str):
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


def handle_package(path: str):
    stdlib = get_stdlib()
    collector = ImportCollector(ignore=[os.path.basename(path)])
    for mod in gather_modules(path):
        path = mod.module_finder.path
        if mod.ispkg:
            continue
        with open(os.path.join(path, f"{mod.name}.py"), "r") as f:
            mod_str = f.read()
        nodes = ast.parse(mod_str)
        collector.visit(nodes)

    final = collector.imports - stdlib
    for mod in sorted(final):
        print(mod)


def handle_notebook(path: str):
    """Parse cells from a notebook, extracting imports."""
    stdlib = get_stdlib()
    with open(path) as ipy_file:
        data = json.load(ipy_file)
    # TODO: check this is a python notebook
    # meta = data['metadata']
    collector = ImportCollector()
    for cell in iter_code_cells(data["cells"]):
        nodes = ast.parse(cell)
        collector.visit(nodes)

    final = collector.imports - stdlib
    for mod in sorted(final):
        print(mod)


def main():
    parser = argparse.ArgumentParser(
        description="Print non-standard-library imports made in a package, module or Jupyter notebook"
    )
    parser.add_argument("path")
    args = parser.parse_args()

    path = os.path.abspath(os.path.expanduser(args.path))
    if os.path.isdir(path):
        handle_package(path)
    elif path.endswith(".ipynb"):
        handle_notebook(path)
    else:
        print(f"Unrecognised path: {args.path}")
        return


if __name__ == "__main__":
    main()
