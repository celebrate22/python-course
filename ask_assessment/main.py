# import ast

# def list_functions(file_path):
#     with open(file_path, "r", encoding="utf-8") as file:
#         tree = ast.parse(file.read(), filename=file_path)

#     for node in ast.walk(tree):
#         if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
#             print(f"function_name: {node.name}, line_number: {node.lineno}")

# list_functions("sample.py")

"""
Rewrite it so it returns a list of dictionaries, one per function, each with name, start_line, end_line, and parent_class (None for top-level functions), sorted in file order.

The tricky part is the parent class. ast.walk won’t tell you a node’s parent. Think about two approaches: looping through tree.body and handling classes separately, or an ast.NodeVisitor where you track which class you’re currently inside. Try one and tell me which you picked and why.

Then write a pytest test using a tiny sample file like the one above, where you know the right answer. Writing the expected result by hand first is the algorithm habit from before.

Paste what you get, including anything that fails."""
import pprint

# ... your extract_functions code above ...
import ast

FUNC_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)

def extract_functions_body(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    results = []
    for node in tree.body:
        if isinstance(node, FUNC_TYPES):
            results.append({
                "name": node.name,
                "start_line": node.lineno,
                "end_line": node.end_lineno,
                "parent_class": None,
            })
        elif isinstance(node, ast.ClassDef):
            for child in node.body:
                if isinstance(child, FUNC_TYPES):
                    results.append({
                        "name": child.name,
                        "start_line": child.lineno,
                        "end_line": child.end_lineno,
                        "parent_class": node.name,
                    })

    return results



if __name__ == "__main__":
    functions = extract_functions_body("sample.py")  # Replace with your exact function name
    pprint.pprint(functions)
