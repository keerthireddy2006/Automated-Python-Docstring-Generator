def coverage_report(parsed_data):
    functions = parsed_data.get("functions", [])
    classes = parsed_data.get("classes", [])

    total_functions = len(functions)
    documented_functions = sum(f["has_docstring"] for f in functions)

    total_methods = sum(len(cls["methods"]) for cls in classes)
    documented_methods = sum(
        m["has_docstring"]
        for cls in classes
        for m in cls["methods"]
    )

    total_classes = len(classes)
    documented_classes = sum(cls["has_docstring"] for cls in classes)

    total_items = total_functions + total_methods
    documented_items = documented_functions + documented_methods
    missing_items = total_items - documented_items

    return {
        # Overall
        "Total Functions & Methods": total_items,
        "Documented": documented_items,
        "Missing Docstrings": missing_items,
        "Coverage (%)": (documented_items / total_items * 100) if total_items else 0,

        # Functions
        "Total Functions": total_functions,
        "Documented Functions": documented_functions,
        "Function Coverage (%)": (documented_functions / total_functions * 100) if total_functions else 0,

        # Methods
        "Total Methods": total_methods,
        "Documented Methods": documented_methods,
        "Method Coverage (%)": (documented_methods / total_methods * 100) if total_methods else 0,

        # Classes
        "Total Classes": total_classes,
        "Documented Classes": documented_classes,
        "Class Coverage (%)": (documented_classes / total_classes * 100) if total_classes else 0
    }
