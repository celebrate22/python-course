
"""Task and TaskList: a task has complete() and __str__(); tasks live in a list."""

from typing import List


class Task:
    def __init__(self, id: int, description: str, done: bool = False):
        self.id = id
        self.description = description
        self.done = done

    def complete(self) -> None:
        """Mark this task as done."""
        self.done = True

    def __str__(self) -> str:
        status = "x" if self.done else " "
        return f"[{status}] {self.id}. {self.description}"


class TaskList:
    """A list of tasks."""

    def __init__(self):
        self._tasks: List[Task] = []

    def add(self, description: str) -> Task:
        task = Task(id=len(self._tasks) + 1, description=description)
        self._tasks.append(task)
        return task

    def complete(self, id: int) -> bool:
        """Mark the task with the given id as done. Returns False if not found."""
        for task in self._tasks:
            if task.id == id:
                task.complete()
                return True
        return False

    def __str__(self) -> str:
        return "\n".join(str(task) for task in self._tasks)

    def __iter__(self):
        return iter(self._tasks)

    def __getitem__(self, index):
        return self._tasks[index]


def main():
    tasks = TaskList()

    tasks.add("Write report")
    tasks.add("Review pull request")
    tasks.add("Buy groceries")

    tasks.complete(2)

    print("Task list:")
    print(tasks)

    print("\nSingle task:")
    print(tasks[0])


if __name__ == "__main__":
    main()
