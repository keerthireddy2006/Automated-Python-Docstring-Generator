import ast
from autodocstring.llm_generator import generate_docstring_llm


class DocstringInjector(ast.NodeTransformer):
    """Injects clean PEP 257 docstrings into functions and methods."""

    def __init__(self, style: str = "Google"):
        self.style = style

    def visit_FunctionDef(self, node):
        self.generic_visit(node)

        try:
            source = ast.unparse(node)
            raw_body = generate_docstring_llm(source, self.style)

            # Strip any triple quotes the LLM might have added
            body = raw_body.strip()
            for q in ['"""', "'''"]:
                if body.startswith(q) and body.endswith(q):
                    body = body[len(q) : -len(q)].strip()

            # Remove any leading/trailing junk
            body = body.strip()

            # Build clean docstring (we add the quotes here only once)
            docstring = f"\n{    body}\n    "

            doc_node = ast.Expr(value=ast.Constant(value=docstring))

            # Replace existing docstring or insert at the beginning
            if node.body and isinstance(node.body[0], ast.Expr):
                if isinstance(node.body[0].value, ast.Constant) and isinstance(
                    node.body[0].value.value, str
                ):
                    # Replace old docstring
                    node.body[0] = doc_node
                else:
                    # Insert new one
                    node.body.insert(0, doc_node)
            else:
                node.body.insert(0, doc_node)

        except Exception as e:
            print(f"Docstring generation failed for {node.name}: {e}")

        return node


def inject_docstrings(source_code: str, style: str = "Google") -> str:
    """
    Parse source code and inject docstrings into all functions/methods.
    """
    try:
        tree = ast.parse(source_code)
    except SyntaxError as e:
        raise SyntaxError(f"Invalid Python code: {str(e)}")

    transformer = DocstringInjector(style=style)
    new_tree = transformer.visit(tree)

    ast.fix_missing_locations(new_tree)
    return ast.unparse(new_tree)
