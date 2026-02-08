from src.compliance import analyze_docstring


def coverage_report(parsed_data):
    functions = parsed_data["functions"]
    classes = parsed_data["classes"]
    methods = [m for c in classes for m in c["methods"]]
    all_items = functions + methods
    missing = {"Parameters": 0, "Returns": 0, "Raises": 0, "Yields": 0, "Attributes": 0}
    compliant = 0
    # ✅ NEW: collect non-compliant details
    non_compliant_items = []

    for item in all_items:
        result = analyze_docstring(item)

        if result["pep257_compliant"]:
            compliant += 1
        else:
            non_compliant_items.append(
                {
                    "Name": (
                        item["name"]
                        if not item.get("class")
                        else f"{item['class']}.{item['name']}"
                    ),
                    "Type": "Method" if item.get("class") else "Function",
                    "Missing Sections": ", ".join(result["missing_sections"]) or "None",
                    "Formatting Issues": ", ".join(result.get("formatting_issues", []))
                    or "None",
                }
            )

        for sec in result["missing_sections"]:
            missing[sec] += 1

    total = len(all_items)
    documented = sum(i["has_docstring"] for i in all_items)
    # ---------- TYPE-WISE COUNTS ----------
    documented_functions = sum(f["has_docstring"] for f in functions)
    documented_methods = sum(m["has_docstring"] for m in methods)
    documented_classes = sum(c["has_docstring"] for c in classes)
    return {
        # ---------- COUNTS ----------
        "Functions": len(functions),
        "Classes": len(classes),
        "Methods": len(methods),
        "Total": total,
        # ---------- OVERALL COVERAGE ----------
        "Documented": documented,
        "Missing": total - documented,
        "Coverage (%)": (documented / total * 100) if total else 0,
        # ---------- TYPE-WISE COVERAGE ----------
        "Function Coverage (%)": (
            documented_functions / len(functions) * 100 if functions else 0
        ),
        "Method Coverage (%)": (
            documented_methods / len(methods) * 100 if methods else 0
        ),
        "Class Coverage (%)": (
            documented_classes / len(classes) * 100 if classes else 0
        ),
        # ---------- COMPLIANCE ----------
        "PEP-257 Compliant": compliant,
        "PEP-257 Compliance (%)": (compliant / total * 100) if total else 0,
        # ---------- MISSING SECTIONS ----------
        **{f"Missing {k}": v for k, v in missing.items()},
        # ---------- ✅ NEW ADDITION ----------
        "Non-Compliant Items": non_compliant_items,
    }
