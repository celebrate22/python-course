import ast

def list_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=file_path)

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            print(f"function_name: {node.name}, line_number: {node.lineno}")



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



"""
Make the function handle any depth of nesting, and record a qualified name for each result, like A.B.deep or outer.inner, instead of a single parent_class. 
Think about whether recursion or a NodeVisitor with a stack of enclosing names fits better, 
since your current approach was always going to struggle here. Also note that if, try and with blocks contain statements too.
"""

import ast
import pprint

class QualifiedFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.results = []
        self.scope = []

    def visit_ClassDef(self, node):
        self.scope.append(node.name)
        try:
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_FunctionDef(self, node):
        self.scope.append(node.name)
        try:
            self.results.append({
                "name": node.name,
                "qualified_name": ".".join(self.scope),
                "start_line": node.lineno,
                "end_line": node.end_lineno,
            })
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)

def extract_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), filename=str(file_path))

    visitor = QualifiedFunctionVisitor()
    visitor.visit(tree)
    return sorted(visitor.results, key=lambda item: item["start_line"])

"""
Write a pytest test. Use a snippet like the example above as a string, 
write the expected list by hand first, and assert that your function returns it. 
You’ll likely have to split the function in two to do this, which is the lesson
"""

import ast
import pprint


class QualifiedFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.results = []
        self.scope = []

    def visit_ClassDef(self, node):
        self.scope.append(node.name)
        try:
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_FunctionDef(self, node):
        self.scope.append(node.name)
        try:
            self.results.append({
                "name": node.name,
                "qualified_name": ".".join(self.scope),
                "start_line": node.lineno,
                "end_line": node.end_lineno,
            })
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


def extract_functions_from_source(source, filename="<string>"):
    tree = ast.parse(source, filename=filename)
    visitor = QualifiedFunctionVisitor()
    visitor.visit(tree)
    return sorted(visitor.results, key=lambda item: item["start_line"])


def extract_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()
    return extract_functions_from_source(source, filename=str(file_path))


"""Split your test into small ones, including an async case.
Write the failing decorator test, then fix the code.
Add a test for a file with a syntax error, and decide what the function should do."""

import ast
import pprint


class QualifiedFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.results = []
        self.scope = []

    def visit_ClassDef(self, node):
        self.scope.append(node.name)
        try:
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_FunctionDef(self, node):
        self.scope.append(node.name)
        try:
            start_line = (
                node.decorator_list[0].lineno
                if node.decorator_list
                else node.lineno
            )
            self.results.append({
                "name": node.name,
                "qualified_name": ".".join(self.scope),
                "start_line": start_line,
                "end_line": node.end_lineno,
            })
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


def extract_functions_from_source(source, filename="<string>"):
    try:
        tree = ast.parse(source, filename=filename)
    except SyntaxError:
        return []

    visitor = QualifiedFunctionVisitor()
    visitor.visit(tree)
    return sorted(visitor.results, key=lambda item: item["start_line"])


def extract_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()
    return extract_functions_from_source(source, filename=str(file_path))

"""Other gaps

Reading files can fail too. Real repos contain files that aren’t UTF-8, and open(...) will raise UnicodeDecodeError on them.
A file that disappears or can’t be opened raises another error. Rare parse failures beyond SyntaxError exist too, 
so the walker must expect surprises from individual files and keep going.
No test for empty source or a file with no functions. Once errors raise, [] will finally mean exactly one thing, so pin that down.
Still unanswered: I’d like to know whether you found a case where sorted matters. If you can’t make one, delete it."""

import ast
import pprint


class QualifiedFunctionVisitor(ast.NodeVisitor):
    def __init__(self):
        self.results = []
        self.scope = []

    def visit_ClassDef(self, node):
        self.scope.append(node.name)
        try:
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_FunctionDef(self, node):
        self.scope.append(node.name)
        try:
            start_line = (
                node.decorator_list[0].lineno
                if node.decorator_list
                else node.lineno
            )
            self.results.append({
                "name": node.name,
                "qualified_name": ".".join(self.scope),
                "start_line": start_line,
                "end_line": node.end_lineno,
            })
            self.generic_visit(node)
        finally:
            self.scope.pop()

    def visit_AsyncFunctionDef(self, node):
        self.visit_FunctionDef(node)


def extract_functions_from_source(source, filename="<string>"):
    tree = ast.parse(source, filename=filename)
    visitor = QualifiedFunctionVisitor()
    visitor.visit(tree)
    return visitor.results


def extract_functions(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        source = file.read()
    return extract_functions_from_source(source, filename=str(file_path))


if __name__ == "__main__":
    pprint.pprint(extract_functions("sample.py"))
