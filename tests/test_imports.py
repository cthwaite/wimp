import ast
from wimp.__main__ import ImportCollector

def test_import_collector_basic():
    code = """
import os
import sys
from pathlib import Path
"""
    collector = ImportCollector()
    nodes = ast.parse(code)
    collector.visit(nodes)
    assert collector.imports == {"os", "sys", "pathlib"}

def test_import_collector_with_ignore():
    code = """
import os
import mypackage
from mypackage.submodule import thing
"""
    collector = ImportCollector(ignore=["mypackage"])
    nodes = ast.parse(code)
    collector.visit(nodes)
    assert collector.imports == {"os"}

def test_import_collector_nested():
    code = """
from os.path import join
from package.subpackage.module import function
"""
    collector = ImportCollector()
    nodes = ast.parse(code)
    collector.visit(nodes)
    assert collector.imports == {"os", "package"}
