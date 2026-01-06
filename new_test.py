import pytest
import json
import os
import subprocess
import sys
from pathlib import Path

def test_script_output():
    repo_root = Path(__file__).resolve().parents[0]
    output_path = repo_root / "output.json"

    result = subprocess.run(
        [sys.executable, "-m", "main"],
        cwd=repo_root,
        capture_output=True,
        text=True
    )

    assert result.returncode == 0, (
        f"Return code: {result.returncode}\n"
        f"cwd used: {repo_root}\n"
        f"STDOUT:\n{result.stdout}\n"
        f"STDERR:\n{result.stderr}\n"
    )

    assert output_path.exists(), "output.json was not created"

    with open(output_path) as f:
        main_output = json.load(f)

    assert "average_final" in main_output
    assert "unique_students" in main_output

    assert main_output["average_final"] == pytest.approx(87.333333, rel=1e-6)
    assert main_output["unique_students"] == 3
