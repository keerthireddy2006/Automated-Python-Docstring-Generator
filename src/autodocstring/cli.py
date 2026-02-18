import sys
import argparse
from pathlib import Path

from autodocstring.parser import parse_file
from autodocstring.coverage import coverage_report


def main():
    parser = argparse.ArgumentParser(
        description="Docstring coverage checker and reporter",
        epilog="Example: python cli.py samples/ --style Google --min-coverage 80 --verbose",
    )
    parser.add_argument(
        "paths",
        nargs="*",
        default=["samples"],
        help="Path(s) to check (folder or files). Default: samples",
    )
    parser.add_argument(
        "--min-coverage",
        type=float,
        default=80.0,
        help="Minimum coverage per file (default: 80.0)",
    )
    parser.add_argument(
        "--style",
        default="Google",
        choices=["Google", "NumPy", "reST"],
        help="Docstring style (default: Google)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed output for each file",
    )

    args = parser.parse_args()

    files = []
    for p in args.paths:
        path = Path(p)
        if path.is_dir():
            files.extend(path.rglob("*.py"))
        elif path.is_file() and path.suffix.lower() == ".py":
            files.append(path)
        else:
            if args.verbose:
                print(f"Skipping non-Python path: {path}")

    if not files:
        print("No Python files found.")
        sys.exit(1)

    failed = []
    print(f"Checking {len(files)} file(s)")

    for file_path in files:
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


if __name__ == "__main__":
    main()
