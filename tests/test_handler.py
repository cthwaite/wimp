import os
import pytest
from pathlib import Path
from wimp.handler import (
    get_handler,
    ModuleHandler,
    JupyterHandler,
    is_neither_magic_nor_shell,
    iter_code_cells
)

def test_get_handler(tmp_path):
    # Test directory handler
    os.makedirs(tmp_path / "test_pkg")
    assert isinstance(get_handler(str(tmp_path)), ModuleHandler)
    
    # Test notebook handler
    nb_path = tmp_path / "test.ipynb"
    nb_path.touch()
    assert isinstance(get_handler(str(nb_path)), JupyterHandler)
    
    # Test invalid path
    with pytest.raises(ValueError):
        get_handler("nonexistent_path")

def test_is_neither_magic_nor_shell():
    assert is_neither_magic_nor_shell("print('hello')")
    assert not is_neither_magic_nor_shell("%matplotlib inline")
    assert not is_neither_magic_nor_shell("!ls")

def test_iter_code_cells():
    notebook = {
        "cells": [
            {"cell_type": "code", "source": ["print('hello')"]},
            {"cell_type": "markdown", "source": ["# Title"]},
            {"cell_type": "code", "source": ["%matplotlib inline"]},
        ]
    }
    cells = list(iter_code_cells(notebook["cells"]))
    assert len(cells) == 2
    assert cells[0] == "print('hello')"
    assert cells[1] == ""
