import pytest
from wimp.__main__ import main
import sys
from unittest.mock import patch

def test_cli_help():
    with pytest.raises(SystemExit) as exc_info:
        with patch.object(sys, 'argv', ['wimp', '--help']):
            main()
    assert exc_info.value.code == 0

def test_cli_invalid_path():
    with patch.object(sys, 'argv', ['wimp', 'nonexistent_path']):
        with patch('builtins.print') as mock_print:
            main()
            mock_print.assert_called_with("Unrecognised path: nonexistent_path")

def test_cli_verbose(tmp_path):
    test_file = tmp_path / "test.py"
    test_file.write_text("import os\nimport sys\n")
    
    with patch.object(sys, 'argv', ['wimp', '-v', str(test_file)]):
        with patch('builtins.print') as mock_print:
            main()
