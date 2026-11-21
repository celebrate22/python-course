from main import extract_functions_from_source


def test_top_level_and_control_blocks():
    source = """try:
    import ujson as json
except ImportError:
    def json_fallback():
        pass

if __name__ == "__main__":
    def main():
        pass
"""
    expected = [
        {"name": "json_fallback", "qualified_name": "json_fallback", "start_line": 4, "end_line": 5},
        {"name": "main", "qualified_name": "main", "start_line": 8, "end_line": 9},
    ]
    assert extract_functions_from_source(source) == expected


def test_nested_classes_and_functions():
    source = """def outer():
    def inner():
        pass

class A:
    class B:
        def deep(self):
            pass
"""
    expected = [
        {"name": "outer", "qualified_name": "outer", "start_line": 1, "end_line": 3},
        {"name": "inner", "qualified_name": "outer.inner", "start_line": 2, "end_line": 3},
        {"name": "deep", "qualified_name": "A.B.deep", "start_line": 7, "end_line": 8},
    ]
    assert extract_functions_from_source(source) == expected


def test_async_functions():
    source = """class Client:
    async def fetch(self):
        return await something()
"""
    expected = [
        {"name": "fetch", "qualified_name": "Client.fetch", "start_line": 2, "end_line": 3},
    ]
    assert extract_functions_from_source(source) == expected


def test_decorated_function_starts_at_first_decorator():
    source = """@login_required
@cache(timeout=60)
def dashboard(request):
    return "ok"
"""
    # Without the decorator_list fix, start_line would be 3 instead of 1
    expected = [
        {"name": "dashboard", "qualified_name": "dashboard", "start_line": 1, "end_line": 4},
    ]
    assert extract_functions_from_source(source) == expected


def test_syntax_error_returns_empty_list():
    broken_source = """def broken_func(x, y:
    return x +
"""
    assert extract_functions_from_source(broken_source) == []
if __name__ == "__main__":
    test_top_level_and_control_blocks()
    test_nested_classes_and_functions()
    test_async_functions()
    test_decorated_function_starts_at_first_decorator()
    test_syntax_error_returns_empty_list()
    print("All tests passed!")
