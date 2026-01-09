def generate_docstring(func, class_name=None):
    title = f"{class_name}.{func['name']}" if class_name else func["name"]

    docstring = f'"""\n{title} function.\n\nParameters:\n'

    if func["params"]:
        for param in func["params"]:
            docstring += f"    {param['name']} : {param['type'] or 'Any'}\n"
    else:
        docstring += "    None\n"

    docstring += "\nReturns:\n"
    docstring += f"    {func['returns'] or 'None'}\n"
    docstring += '"""'

    return docstring
