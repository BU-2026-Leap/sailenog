import pytest

import json
import os
import subprocess
import sys
from pathlib import Path
def test_script_output():
    repo_root = Path(__file__).resolve().parents[0]
    print("repo: " + str(repo_root))
    output_filename = "output.json"

    result = subprocess.run(
        [sys.executable, "-m", "main"],
        cwd=str(repo_root),
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Return code: {result.returncode}\n"
        f"cwd used: {repo_root}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}\n"
    )

    assert os.path.exists(output_filename)

    with open(output_filename) as f:
        main_output = json.load(f)

        assert "average_final" in main_output
        # TODO: write more assertions here
        assert "unique_students" == 3 in main_output
