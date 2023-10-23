from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from task import Task, load_tasks, save_tasks


@contextmanager
def edit_tasks(filename: Path) -> Generator[list[Task], None, None]:
    # Load tasks
    try:
        with open(filename, "r") as f:
            tasks = load_tasks(f)
    except OSError:
        tasks = []

    # Give access to the tasks to the user
    try:
        yield tasks

    # Save the edits made by the user
    finally:
        # Save the new task list
        with open(filename, "w") as f:
            save_tasks(f, tasks)
