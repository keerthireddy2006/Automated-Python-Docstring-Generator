def _summary(item, class_name=None):
    if "name" in item:
        name = f"{class_name}.{item['name']}" if class_name else item["name"]
    else:
        name = "Object"

    return f"Generate documentation for {name}."


def generate_google(func, class_name=None):
    doc = f"{_summary(func, class_name)}\n\n"

    if func.get("params"):
        doc += "Args:\n"
        for p in func["params"]:
            doc += f"    {p['name']} ({p['type'] or 'Any'}): Description.\n"

    if func.get("returns"):
        doc += f"\nReturns:\n    {func['returns']}: Description.\n"

    if func.get("raises"):
        doc += "\nRaises:\n"
        for r in func["raises"]:
            doc += f"    {r}: Description.\n"

    if func.get("is_generator"):
        doc += "\nYields:\n    value: Generated value.\n"

    return doc.strip()


def generate_numpy(func, class_name=None):
    doc = f"{_summary(func, class_name)}\n\n"

    if func.get("params"):
        doc += "Parameters\n----------\n"
        for p in func["params"]:
            doc += f"{p['name']} : {p['type'] or 'Any'}\n    Description.\n"

    if func.get("returns"):
        doc += f"\nReturns\n-------\n{func['returns']}\n    Description.\n"

    if func.get("raises"):
        doc += "\nRaises\n------\n"
        for r in func["raises"]:
            doc += f"{r}\n    Description.\n"

    if func.get("is_generator"):
        doc += "\nYields\n------\nvalue\n    Generated value.\n"

    return doc.strip()


def generate_rest(func, class_name=None):
    doc = f"{_summary(func, class_name)}\n\n"

    for p in func.get("params", []):
        doc += f":param {p['name']}: Description.\n"
        doc += f":type {p['name']}: {p['type'] or 'Any'}\n"

    if func.get("returns"):
        doc += f":return: {func['returns']}.\n"

    for r in func.get("raises", []):
        doc += f":raises {r}: Description.\n"

    if func.get("is_generator"):
        doc += ":yields: Generated value.\n"

    return doc.strip()


def generate_docstring(func, class_name=None, style="Google"):
    if style == "NumPy":
        return generate_numpy(func, class_name)
    if style == "reST":
        return generate_rest(func, class_name)
    return generate_google(func, class_name)
