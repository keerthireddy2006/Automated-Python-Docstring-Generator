import subprocess
import re

CATEGORY_MAP = {
    "D10": "Missing Docstrings",
    "D20": "Whitespace Issues",
    "D30": "Quotes Issues",
    "D40": "Docstring Content Issues",
}


def categorize(code):
    for k in CATEGORY_MAP:
        if code.startswith(k):
            return CATEGORY_MAP[k]
    return "Other"


def run_full_pep257(file_path):
    result = subprocess.run(["pydocstyle", file_path], capture_output=True, text=True)

    issues = []

    for line in result.stdout.splitlines():

        match = re.match(r"(.*?):(\d+)\s+(D\d+)\s+(.*)", line)

        if match:
            code = match.group(3)

            issues.append(
                {
                    "File": match.group(1),
                    "Line": int(match.group(2)),
                    "Code": code,
                    "Category": categorize(code),
                    "Message": match.group(4),
                    "Fix": suggest_fix(code),
                }
            )

    return issues


# Only SAFE automatic fixes
def suggest_fix(code):

    fixes = {
        "D100": "Add module docstring at top of file",
        "D101": "Add class docstring",
        "D102": "Add method docstring",
        "D103": "Add function docstring",
        "D205": "Add blank line after summary",
        "D400": "End summary with period",
        "D401": "Use imperative mood",
        "D403": "Capitalize first word",
        "D404": "Avoid starting with 'This'",
    }

    return fixes.get(code, "Manual fix required")
