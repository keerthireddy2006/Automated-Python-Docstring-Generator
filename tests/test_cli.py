import pytest
import subprocess
import sys


def test_cli_help():
    result = subprocess.run(
        [sys.executable, "-m", "autodocstring.cli", "--help"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, f"CLI failed:\n{result.stderr}"
    assert "Docstring coverage checker" in result.stdout
    assert "--style" in result.stdout
    assert "--min-coverage" in result.stdout


def test_cli_default(tmp_path):
    dummy_file = tmp_path / "dummy.py"
    dummy_file.write_text("def hello(): pass")  # No docstring → should fail coverage

    result = subprocess.run(
        [sys.executable, "-m", "autodocstring.cli", str(dummy_file), "--verbose"],
        capture_output=True,
        text=True,
    )

    # Now expect failure (exit code 1) because coverage < 80%
    assert result.returncode == 1, f"Unexpected success: {result.stdout}"
    assert "Checking 1 file(s)" in result.stdout
    assert "dummy.py: 0.00%" in result.stdout
    assert "missing 1 items" in result.stdout
    assert "Failed: 1 file(s)" in result.stdout
