import os

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