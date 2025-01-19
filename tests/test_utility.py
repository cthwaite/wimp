import sys
from wimp.utility import get_stdlib, gather_modules

def test_get_stdlib():
    stdlib = get_stdlib()
    assert isinstance(stdlib, set)
    assert "os" in stdlib
    assert "sys" in stdlib
    assert "pathlib" in stdlib
    assert "pytest" not in stdlib  # Not a stdlib module

def test_gather_modules(tmp_path):
    # Create a simple package structure
    pkg_dir = tmp_path / "test_pkg"
    pkg_dir.mkdir()
    (pkg_dir / "__init__.py").touch()
    (pkg_dir / "module1.py").write_text("import os")
    
    subpkg_dir = pkg_dir / "subpkg"
    subpkg_dir.mkdir()
    (subpkg_dir / "__init__.py").touch()
    (subpkg_dir / "module2.py").write_text("import sys")
    
    modules = list(gather_modules(str(pkg_dir)))
    assert len(modules) > 0
    module_names = {mod.name for mod in modules}
    assert "module1" in module_names
    assert "subpkg.module2" in module_names
