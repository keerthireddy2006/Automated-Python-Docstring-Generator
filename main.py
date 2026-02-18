import argparse
from autodocstring.parser import parse_file
from autodocstring.generator import generate_docstring
from autodocstring.coverage import coverage_report


def main():
    parser = argparse.ArgumentParser(
        description="Automated Python Docstring Generator (CLI)"
    )

    parser.add_argument("path", help="Path to the Python file to analyze")

    args = parser.parse_args()
    parsed_data = parse_file(args.path)

    print("\nGenerated Docstrings:\n")

    # Standalone functions
    if parsed_data["functions"]:
        print("\nStandalone Functions:")
        print("-" * 21)

        for func in parsed_data["functions"]:
            if not func["has_docstring"]:
                print(generate_docstring(func))
                print("-" * 40)

    # Class methods
    for cls in parsed_data["classes"]:
        print(f"\nClass: {cls['class_name']}\n")
        for method in cls["methods"]:
            if not method["has_docstring"]:
                print(generate_docstring(method, cls["class_name"]))
                print("-" * 40)

    report = coverage_report(parsed_data)
    print("\nDocstring Coverage Report:")
    print("-" * 26)
    for key, value in report.items():
        print(f"{key:<25}: {value}")


if __name__ == "__main__":
    main()
