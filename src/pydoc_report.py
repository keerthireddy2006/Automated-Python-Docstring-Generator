import subprocess


def run_pydocstyle(file_path):
    """
    Runs pydocstyle and returns RAW violations.
    This version is FAIL-SAFE.
    """

    try:
        result = subprocess.run(
            ["pydocstyle", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        output = result.stdout + result.stderr

        if not output.strip():
            return []

        issues = []

        for line in output.splitlines():
            issues.append({"Violation": line})

        return issues

    except Exception as e:
        return [{"Violation": str(e)}]
