""" """

import ast
import contextlib
from ast import NodeVisitor
from typing import Generator, Self


_TRANSLATE = {
    "pkg_resources": "setuptools",
}


class ImportCollector(NodeVisitor):
    def __init__(self, ignore: list[str] | None = None) -> None:
        super().__init__()
        self.imports = set()
        self._ignore = set(ignore) if ignore else set()

    @contextlib.contextmanager
    def ignore(self, *ignore: str) -> Generator[Self, None, None]:
        old_ignore = self._ignore
        self._ignore |= set(ignore)
        yield self
        self._ignore = old_ignore

    def _push_name(self, name: str) -> None:
        if name not in self._ignore:
            self.imports.add(_TRANSLATE.get(name, name))

    def visit_Import(self, node: ast.Import) -> None:
        for alias in node.names:
            name, *_ = alias.name.split(".")
            self._push_name(name)

    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        if node.module is not None:
            name = node.module
            if "." in name:
                name, *_ = name.split(".")
            if node.level == 0:
                self._push_name(name)
