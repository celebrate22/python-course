from main import extract_functions_from_source

SAMPLE_SOURCE = """import os

try:
    import ujson as json
except ImportError:
    def json_fallback(): ...

def outer():
    def inner(): ...

class A:
    class B:
        def deep(self): ...

if __name__ == "__main__":
    def main(): ...
"""

EXPECTED = [
    {
        "name": "json_fallback",
        "qualified_name": "json_fallback",
        "start_line": 6,
        "end_line": 6,
    },
    {
        "name": "outer",
        "qualified_name": "outer",
        "start_line": 8,
        "end_line": 9,
    },
    {
        "name": "inner",
        "qualified_name": "outer.inner",
        "start_line": 9,
        "end_line": 9,
    },
    {
        "name": "deep",
        "qualified_name": "A.B.deep",
        "start_line": 13,
        "end_line": 13,
    },
    {
        "name": "main",
        "qualified_name": "main",
        "start_line": 16,
        "end_line": 16,
    },
]


def test_extract_functions_from_source():
    assert extract_functions_from_source(SAMPLE_SOURCE) == EXPECTED
