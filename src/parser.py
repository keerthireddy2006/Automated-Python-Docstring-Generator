import ast


class CodeParser(ast.NodeVisitor):
    def __init__(self):
        self.functions = []
        self.classes = []
        self.current_class = None

    # ---------- TOP-LEVEL FUNCTIONS ----------
    def visit_FunctionDef(self, node):
        if self.current_class is None:
            self.functions.append(self.extract_function(node))
        self.generic_visit(node)

    # ---------- CLASSES ----------
    def visit_ClassDef(self, node):
        class_docstring = ast.get_docstring(node)

        class_info = {
            "class_name": node.name,
            "has_docstring": class_docstring is not None,
            "docstring": class_docstring,
            "attributes": [],
            "methods": [],
        }

        self.current_class = node.name

        for item in node.body:
            if isinstance(item, ast.Assign):
                for target in item.targets:
                    if isinstance(target, ast.Name):
                        class_info["attributes"].append(target.id)

            if isinstance(item, ast.FunctionDef):
                class_info["methods"].append(self.extract_function(item, node.name))

        self.classes.append(class_info)
        self.current_class = None

    # ---------- FUNCTION EXTRACTION ----------
    def extract_function(self, node, class_name=None):
        docstring = ast.get_docstring(node)

        params = [
            {
                "name": arg.arg,
                "type": ast.unparse(arg.annotation) if arg.annotation else None,
            }
            for arg in node.args.args
        ]

        param_names = [p["name"] for p in params]
        signature = f"{node.name}({', '.join(param_names)})"

        returns = ast.unparse(node.returns) if node.returns else None

        raises = []
        is_generator = False

        for child in ast.walk(node):
            if isinstance(child, ast.Raise):
                raises.append(ast.unparse(child.exc) if child.exc else "Exception")
            if isinstance(child, (ast.Yield, ast.YieldFrom)):
                is_generator = True

        return {
            "name": node.name,
            "class": class_name,
            "signature": signature,  # ⭐ ADDED
            "params": params,
            "returns": returns,
            "has_docstring": docstring is not None,
            "lineno": node.lineno,
            "docstring": docstring,
            "raises": list(set(raises)),
            "is_generator": is_generator,
        }


def parse_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())

    parser = CodeParser()
    parser.visit(tree)

    return {"functions": parser.functions, "classes": parser.classes}
