import ast
from wimp.collector import ImportCollector

def test_import_collector():
    # Basic imports
    code = """
import os
import sys as system
from pathlib import Path
from typing import List, Dict
"""
    collector = ImportCollector()
    nodes = ast.parse(code)
    collector.visit(nodes)
    assert collector.imports == {"os", "sys", "pathlib", "typing"}

def test_import_collector_with_ignore():
    code = """
import os
import sys
"""
    collector = ImportCollector(ignore=["os"])
    nodes = ast.parse(code)
    collector.visit(nodes)
    assert collector.imports == {"sys"}

def test_import_collector_context():
    code = """
import os
import sys
"""
    collector = ImportCollector()
    with collector.ignore("os"):
        nodes = ast.parse(code)
        collector.visit(nodes)
    assert collector.imports == {"sys"}

def test_import_translation():
    code = """
import pkg_resources
"""
    collector = ImportCollector()
    nodes = ast.parse(code)
    collector.visit(nodes)
    assert collector.imports == {"setuptools"}
