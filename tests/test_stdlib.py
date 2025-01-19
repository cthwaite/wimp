from wimp.__main__ import get_stdlib

def test_stdlib_detection():
    stdlib = get_stdlib()
    # Test some known standard library modules
    assert "os" in stdlib
    assert "sys" in stdlib
    assert "json" in stdlib
    assert "ast" in stdlib
    
    # Test that some common third-party packages are not included
    assert "pytest" not in stdlib
    assert "pandas" not in stdlib
    assert "numpy" not in stdlib
