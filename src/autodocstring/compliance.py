def analyze_docstring(func, style=None):
    raw_doc = func.get("docstring") or ""
    doc = raw_doc.lower()
    missing = []
    formatting_issues = []
    warnings = []
    # ---------- SECTION COMPLETENESS ----------
    if func["params"] and not any(k in doc for k in ["param", "args", "parameters"]):
        missing.append("Parameters")

    if func["returns"] and "return" not in doc:
        missing.append("Returns")

    if func["raises"] and "raise" not in doc:
        missing.append("Raises")

    if func["is_generator"] and "yield" not in doc:
        missing.append("Yields")

    if func.get("class") and func.get("attributes") and "attribute" not in doc:
        missing.append("Attributes")
    # ---------- SUMMARY LINE CHECK ----------
    if raw_doc:
        first_line = raw_doc.strip().split("\n")[0].strip()

        if not first_line:
            formatting_issues.append("Empty summary line")
        elif not first_line.endswith("."):
            warnings.append("Summary line should end with a period")
        elif len(first_line) > 72:
            warnings.append("Summary line is too long")
        elif first_line.lower().startswith(
            ("returns", "does", "divides", "calculates")
        ):
            warnings.append("Summary line not in imperative mood")
    else:
        formatting_issues.append("Missing summary line")
    # ---------- STYLE-SPECIFIC CHECK ----------
    if style and raw_doc:
        if style == "Google" and "args:" not in doc:
            warnings.append("Google style expects 'Args:' section")

        if style == "NumPy" and "parameters" not in doc:
            warnings.append("NumPy style expects 'Parameters' section")

        if style == "reST" and ":param" not in doc:
            warnings.append("reST style expects ':param:' fields")
    return {
        "missing_sections": missing,
        "formatting_issues": formatting_issues,
        "warnings": warnings,
        "pep257_compliant": len(missing) == 0 and len(formatting_issues) == 0,
    }
