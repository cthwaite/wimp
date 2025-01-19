import json
import os
import tempfile
from wimp.__main__ import handle_notebook

def test_notebook_parsing():
    notebook_content = {
        "cells": [
            {
                "cell_type": "code",
                "source": ["import pandas as pd\n", "import numpy as np"],
                "outputs": []
            },
            {
                "cell_type": "markdown",
                "source": ["# This is markdown"],
            },
            {
                "cell_type": "code",
                "source": ["from sklearn import metrics"],
                "outputs": []
            }
        ],
        "metadata": {"kernelspec": {"language": "python"}}
    }
    
    with tempfile.NamedTemporaryFile(suffix='.ipynb', mode='w', delete=False) as f:
        json.dump(notebook_content, f)
        temp_path = f.name
    
    try:
        # Capture stdout to test output
        import sys
        from io import StringIO
        captured_output = StringIO()
        sys.stdout = captured_output

        handle_notebook(temp_path)
        
        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip().split('\n')
        assert set(output) == {"numpy", "pandas", "sklearn"}
    
    finally:
        os.unlink(temp_path)
