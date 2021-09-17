"""
"""

import ast
import contextlib
from ast import NodeVisitor
from typing import List, Optional


_TRANSLATE = {
    "pkg_resources": "setuptools",
}


class ImportCollector(NodeVisitor):
    def __init__(self, ignore: Optional[List[str]] = None):
        super().__init__()
        self.imports = set()
        self._ignore = set(ignore) if ignore else set()

    @contextlib.contextmanager
    def ignore(self, *ignore: str):
        old_ignore = self._ignore
        self._ignore |= set(ignore)
        yield self
        self._ignore = old_ignore

    def _push_name(self, name: str):
        if name not in self._ignore:
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
