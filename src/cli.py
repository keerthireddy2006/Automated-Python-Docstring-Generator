import sys
import argparse
from pathlib import Path

from .parser import parse_file
from .coverage import coverage_report


def main():
    parser = argparse.ArgumentParser(description="Docstring coverage checker")
    parser.add_argument(
        "paths",
        nargs="*",
        default=["samples"],
        help="Path(s) to check (folder or files). Default: samples",
    )
    parser.add_argument(
        "--min-coverage", type=float, default=80.0, help="Minimum coverage per file"
    )
    parser.add_argument(
        "--style", default="Google", choices=["Google", "NumPy", "reST"]
    )
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    files = [Path(p) for p in args.paths]

    if not files:
        print("No files or path provided.")
        sys.exit(1)

    failed = []
    print(f"Checking {len(files)} file(s)")

    for file_path in files:
        if not file_path.exists():
            print(f"File not found: {file_path}")
            continue

        if not file_path.is_file() or file_path.suffix != ".py":
            if args.verbose:
                print(f"Skipping non-Python file: {file_path}")
            continue

        try:
            parsed = parse_file(str(file_path))
            report = coverage_report(parsed)

            # Safe access to keys with defaults
            coverage_pct = report.get("Coverage (%)", 0.0)
            missing_count = report.get("Missing", 0)

            if coverage_pct < args.min_coverage:
                failed.append((file_path, coverage_pct, missing_count))
                print(
                    f"  {file_path}: {coverage_pct:.2f}% - missing {missing_count} items"
                )
            else:
                if args.verbose:
                    print(f"  {file_path}: {coverage_pct:.2f}% ✓ OK")

        except Exception as e:
            print(f"Error processing {file_path}: {type(e).__name__}: {str(e)}")
            failed.append((file_path, 0.0, "error"))

    if failed:
        print(
            f"\nFailed: {len(failed)} file(s) below {args.min_coverage}% or had errors"
        )
        sys.exit(1)

    print("All checked files passed coverage check.")
    sys.exit(0)
