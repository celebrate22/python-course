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