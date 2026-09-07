"""
file_handling.py
------------------
A tour of Python's file handling tools, with runnable examples for each
concept, plus a small Log File Manager project at the end.

All demos operate inside a 'demo_workspace' folder created next to this
script, so nothing outside that folder is touched. Run this file directly:
    python file_handling.py
"""

import os
from pathlib import Path


# A single workspace folder all demos write into/read from, kept next to
# this script so re-running the file is repeatable and self-contained.
WORKSPACE = Path(__file__).parent / "demo_workspace"


def setup_workspace():
    """Make sure the workspace folder exists before any demo runs."""
    WORKSPACE.mkdir(exist_ok=True)


# ---------------------------------------------------------------------------
# 1. FILE HANDLING - open(), and why 'with' matters
# ---------------------------------------------------------------------------
def demo_file_handling():
    print("\n=== FILE HANDLING (open / with) ===")
    file_path = WORKSPACE / "hello.txt"

    # 'with' automatically closes the file when the block ends,
    # even if an exception is raised inside it.
    with open(file_path, "w") as f:
        f.write("Hello, file handling!")

    print(f"File closed automatically? {f.closed}")  # True, even outside the block


# ---------------------------------------------------------------------------
# 2. READ FILES
# ---------------------------------------------------------------------------
def demo_read_files():
    print("\n=== READ FILES ===")
    file_path = WORKSPACE / "poem.txt"

    with open(file_path, "w") as f:
        f.write("Roses are red\nViolets are blue\nPython is fun\nAnd so are you\n")

    # .read() - whole file as one string
    with open(file_path, "r") as f:
        content = f.read()
    print("Full content:\n" + content)

    # .readlines() - list of lines (each includes the trailing \n)
    with open(file_path, "r") as f:
        lines = f.readlines()
    print("Number of lines:", len(lines))

    # Iterating line by line - most memory-efficient for large files,
    # since it doesn't load the whole file into memory at once
    print("Iterating line by line:")
    with open(file_path, "r") as f:
        for i, line in enumerate(f, start=1):
            print(f"  {i}: {line.strip()}")


# ---------------------------------------------------------------------------
# 3. WRITE / CREATE FILES
# ---------------------------------------------------------------------------
def demo_write_files():
    print("\n=== WRITE / CREATE FILES ===")
    file_path = WORKSPACE / "notes.txt"

    # "w" - creates the file if it doesn't exist, OVERWRITES if it does
    with open(file_path, "w") as f:
        f.write("First note\n")
    print("After 'w' mode:", file_path.read_text().strip())

    # "a" - appends without overwriting existing content
    with open(file_path, "a") as f:
        f.write("Second note\n")
    print("After 'a' mode:\n" + file_path.read_text())

    # "x" - exclusive creation, fails if the file already exists
    try:
        with open(file_path, "x") as f:
            f.write("This will not happen")
    except FileExistsError as e:
        print("'x' mode correctly refused to overwrite:", e)


# ---------------------------------------------------------------------------
# 4. OS MODULE
# ---------------------------------------------------------------------------
def demo_os_module():
    print("\n=== OS MODULE ===")
    workspace_str = str(WORKSPACE)

    print("Does workspace exist?", os.path.exists(workspace_str))
    print("Is it a directory?", os.path.isdir(workspace_str))

    # os.path.join builds paths in an OS-independent way (handles / vs \)
    joined = os.path.join(workspace_str, "subfolder", "file.txt")
    print("Joined path:", joined)

    # Listing directory contents
    print("Contents of workspace:", os.listdir(workspace_str))

    # Renaming a file
    old_path = os.path.join(workspace_str, "hello.txt")
    new_path = os.path.join(workspace_str, "greeting.txt")
    if os.path.exists(old_path):
        os.rename(old_path, new_path)
        print(f"Renamed hello.txt -> greeting.txt: {os.path.exists(new_path)}")

    # Reading an environment variable (returns None if not set)
    print("HOME env var:", os.environ.get("HOME", "not set"))


# ---------------------------------------------------------------------------
# 5. PATHLIB MODULE
# ---------------------------------------------------------------------------
def demo_pathlib_module():
    print("\n=== PATHLIB MODULE ===")

    # Path objects support the / operator for joining - reads more naturally
    # than os.path.join()
    file_path = WORKSPACE / "pathlib_demo.txt"
    file_path.write_text("Written using pathlib!")

    print("File exists?", file_path.exists())
    print("File name:", file_path.name)
    print("File suffix:", file_path.suffix)
    print("Parent directory:", file_path.parent)
    print("Content:", file_path.read_text())

    # glob() to find files matching a pattern
    txt_files = list(WORKSPACE.glob("*.txt"))
    print(f"Found {len(txt_files)} .txt files:", [p.name for p in txt_files])


# ---------------------------------------------------------------------------
# 6. DIRECTORY MANAGEMENT
# ---------------------------------------------------------------------------
def demo_directory_management():
    print("\n=== DIRECTORY MANAGEMENT ===")

    nested_dir = WORKSPACE / "reports" / "2026"

    # os.makedirs (with exist_ok=True) creates nested directories in one call
    os.makedirs(nested_dir, exist_ok=True)
    print("Created nested dir with os.makedirs:", nested_dir.exists())

    # pathlib equivalent, using parents=True for nested creation
    another_dir = WORKSPACE / "archive" / "old_logs"
    another_dir.mkdir(parents=True, exist_ok=True)
    print("Created nested dir with pathlib:", another_dir.exists())

    # Listing only directories inside the workspace
    subdirs = [p.name for p in WORKSPACE.iterdir() if p.is_dir()]
    print("Subdirectories in workspace:", subdirs)

    # Removing an empty directory
    another_dir.rmdir()
    print("Removed 'old_logs'? ", not another_dir.exists())


# ---------------------------------------------------------------------------
# PROJECT: Log File Manager
# A small class that creates a dated log directory, writes/appends entries,
# reads them back, and lists all log files - combining open(), pathlib,
# and directory management.
# ---------------------------------------------------------------------------
class LogManager:
    def __init__(self, base_dir):
        self.base_dir = Path(base_dir) / "logs"
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def _log_path(self, log_name):
        return self.base_dir / f"{log_name}.log"

    def write_entry(self, log_name, message):
        """Append a timestamped-style entry to a named log file."""
        path = self._log_path(log_name)
        with open(path, "a") as f:
            f.write(f"[{log_name}] {message}\n")

    def read_log(self, log_name):
        path = self._log_path(log_name)
        if not path.exists():
            return f"No log named '{log_name}' found."
        return path.read_text()

    def list_logs(self):
        return [p.name for p in self.base_dir.glob("*.log")]

    def delete_log(self, log_name):
        path = self._log_path(log_name)
        if path.exists():
            path.unlink()  # pathlib's way of deleting a file
            return True
        return False


def demo_log_manager():
    print("\n=== PROJECT: LOG FILE MANAGER ===")
    manager = LogManager(WORKSPACE)

    manager.write_entry("app", "Application started")
    manager.write_entry("app", "User logged in")
    manager.write_entry("errors", "Failed to connect to database")

    print("Available logs:", manager.list_logs())

    print("\n--- app.log ---")
    print(manager.read_log("app"))

    print("--- errors.log ---")
    print(manager.read_log("errors"))

    deleted = manager.delete_log("errors")
    print(f"Deleted errors.log? {deleted}")
    print("Remaining logs:", manager.list_logs())


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    setup_workspace()
    demo_file_handling()
    demo_read_files()
    demo_write_files()
    demo_os_module()
    demo_pathlib_module()
    demo_directory_management()
    demo_log_manager()
    print(f"\nAll demo files were created under: {WORKSPACE}")