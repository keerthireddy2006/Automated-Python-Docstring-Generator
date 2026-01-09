import ast

class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.current_class = None

    # ---------- TOP-LEVEL FUNCTIONS ----------
    def visit_FunctionDef(self, node):
        if self.current_class is None:
            docstring = ast.get_docstring(node)

            self.functions.append({
                "name": node.name,
                "params": [
                    {
                        "name": arg.arg,
                        "type": ast.unparse(arg.annotation) if arg.annotation else None
                    } for arg in node.args.args
                ],
                "returns": ast.unparse(node.returns) if node.returns else None,
                "has_docstring": docstring is not None,
                "docstring": docstring
            })

        self.generic_visit(node)

    # ---------- CLASSES & METHODS ----------
    def visit_ClassDef(self, node):
        class_docstring = ast.get_docstring(node)

        class_info = {
            "class_name": node.name,
            "has_docstring": class_docstring is not None,
            "docstring": class_docstring,
            "methods": []
        }

        self.current_class = node.name

        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                method_docstring = ast.get_docstring(item)

                class_info["methods"].append({
                    "name": item.name,
                    "params": [
                        {
                            "name": arg.arg,
                            "type": ast.unparse(arg.annotation) if arg.annotation else None
                        } for arg in item.args.args
                    ],
                    "returns": ast.unparse(item.returns) if item.returns else None,
                    "has_docstring": method_docstring is not None,
                    "docstring": method_docstring
                })

        self.classes.append(class_info)
        self.current_class = None


# ---------- REQUIRED ENTRY FUNCTION ----------
def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    parser = CodeParser()
    parser.visit(tree)

    return {
        "functions": parser.functions,
        "classes": parser.classes
    }
