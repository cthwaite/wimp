""" """

import ast
import json
import logging
import os
import sys
import site
from typing import Any, Dict, Generator, List

from .collector import ImportCollector
from .utility import gather_modules


class BaseHandler:
    def __init__(self, path: str):
        self.path = os.path.abspath(os.path.expanduser(path))
        self._log = logging.getLogger(self.__class__.__name__)

    def _handle_source(self, collector: ImportCollector, source: str):
        nodes = ast.parse(source)
        collector.visit(nodes)

    def collect_into(self, collector: ImportCollector):
        raise NotImplementedError


class ModuleHandler(BaseHandler):
    """ """

    def collect_into(self, collector: ImportCollector):
        """ """
        with collector.ignore(os.path.basename(self.path)):
            for mod in gather_modules(self.path):
                if mod.ispkg:
                    continue
                spec = mod.module_finder.find_spec(mod.name)
                if spec is None:
                    self._log.warning("Failed to resolve spec for module %s", mod.name)
                    continue
                name, py_path = spec.name, spec.origin
                if py_path is None:
                    self._log.warning("Failed to get origin for %s", name)
                    continue
                _, ext = os.path.splitext(py_path)
                if ext != ".py":
                    self._log.warning("Skipping module %s at '%s'", name, py_path)
                    continue
                with open(py_path, "r") as f:
                    mod_str = f.read()
                self._log.info("Handling %s", py_path)
                self._handle_source(collector, mod_str)


def is_neither_magic_nor_shell(code: str) -> bool:
    """Check that a string is neither a Jupyter 'magic' command nor a shell invocation."""
    return not (code.startswith("%") or code.startswith("!"))


def iter_code_cells(cells: List[Dict[str, Any]]) -> Generator[str, None, None]:
    """Iterate over cells in a Jupyter notebook, yielding Python code, filtering out
    magic and shell commands.
    """
    for cell in cells:
        if cell["cell_type"] == "code":
            source = cell["source"]
            yield "".join(filter(is_neither_magic_nor_shell, source))


class JupyterHandler(BaseHandler):
    def _handle_one(self, collector, cell: str):
        nodes = ast.parse(cell)
        collector.visit(nodes)

    def collect_into(self, collector: ImportCollector):
        self._log.info("Loading '%s'", self.path)
        with open(self.path) as ipy_file:
            data = json.load(ipy_file)
        meta = data.get("metadata")

        if meta is None:
            self._log.warning("No metadata found for notebook")
        else:
            spec = meta.get("kernelspec", {})
            spec_str = " ".join(f"{key}='{value}'" for key, value in spec.items())
            self._log.info("Got kernel: %s ", spec_str)

        for cell in iter_code_cells(data["cells"]):
            self._handle_source(collector, cell)


def get_handler(path: str):
    """Get the best-fit handler for a string representing a path or module."""
    abs_path = os.path.abspath(os.path.expanduser(path))
    if os.path.isdir(abs_path):
        return ModuleHandler(path)
    elif path.endswith(".ipynb"):
        return JupyterHandler(path)
    else:
        site_packages, *_ = site.getsitepackages()
        mod_path = os.path.join(site_packages, path)
        if os.path.isdir(mod_path):
            return ModuleHandler(mod_path)
        raise ValueError(f"Unable to find handler for path: {path}")
