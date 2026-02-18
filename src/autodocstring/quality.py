import subprocess
import tempfile
import os


def pep257_report(file_path):
    """
    Runs pydocstyle on a Python file and returns:
    - Total errors
    - Error messages
    - Compliance %
    """

    try:
        result = subprocess.run(
            ["pydocstyle", file_path], capture_output=True, text=True
        )

        errors = result.stdout.strip().split("\n") if result.stdout else []
        errors = [e for e in errors if e.strip()]

        return {
            "total_errors": len(errors),
            "messages": errors,
            "compliance": 0 if errors else 100,
        }

    except Exception as e:
        return {"total_errors": 0, "messages": [str(e)], "compliance": 0}
