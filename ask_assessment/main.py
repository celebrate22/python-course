import ast

def list_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            print(f"function_name: {node.name}, line_number: {node.lineno}")

list_functions("sample.py")