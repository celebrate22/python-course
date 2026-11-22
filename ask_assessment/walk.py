"""Given a folder, return a sorted list of paths to every .py file inside it, 
relative to that folder, skipping junk folders."""

def walker(folder):
    with open(folder, "r", encoding="utf-8") as file:

