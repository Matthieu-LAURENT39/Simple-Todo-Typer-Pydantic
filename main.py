from pathlib import Path
from typing import Annotated
from uuid import UUID

import typer

from const import DEFAULT_FILENAME
from task import Task
from utils import edit_tasks

app = typer.Typer()


@app.command()
def list(
    absolute_id: Annotated[
        bool,
        typer.Option(
            "--absolute-id/--no-absolute-id",
            "-a/-A",
            help="Display absolute IDs for tasks, that are garanteed to not change",
        ),
    ] = False,
    file: Annotated[
        Path, typer.Option(help="The file containing the tasks")
    ] = DEFAULT_FILENAME,
):
    """Lists all existing tasks"""
    with edit_tasks(file) as tasks:
        for i, t in enumerate(tasks, start=1):
            print(f"{t.absolute_id if absolute_id else i}: {t}")


@app.command()
def add(
    body: str,
    file: Annotated[
        Path, typer.Option(help="The file containing the tasks")
    ] = DEFAULT_FILENAME,
):
    """Adds a new task to the list"""
    with edit_tasks(file) as tasks:
        tasks.append(
            Task(body=body),
        )
        typer.echo("Task successfully added.")


@app.command()
def done(
    task_id: Annotated[
        str, typer.Argument(help="The ID of the task. Can be relative of absolute.")
    ],
    file: Annotated[
        Path, typer.Option(help="The file containing the tasks")
    ] = DEFAULT_FILENAME,
):
    """Marks a task as done"""
    with edit_tasks(file) as tasks:
        task = None

        # Absolute IDs
        try:
            tid = UUID(task_id)
            task = next(t for t in tasks if t.absolute_id == tid)

        except StopIteration:
            typer.echo("This task doesn't exist!")
            raise typer.Exit(code=1) from None
        except ValueError:
            # The id wasn't absolute, try relative next
            pass

        # Relative IDs
        if task is None:
            try:
                tid = int(task_id)
                if tid <= 0:
                    typer.echo("IDs must be strictly positive!")
                    raise typer.Exit(code=2)
                task = tasks[tid - 1]

            except IndexError:
                typer.echo("This task doesn't exist!")
                raise typer.Exit(code=1) from None
            except ValueError:
                # The id wasn't absolute, move on
                pass

        # ID was invalid
        if task is None:
            typer.echo("Invalid ID! It must be a number or UUID!")
            raise typer.Exit(code=2)
        else:
            tasks.remove(task)
            typer.echo(f"Task {task_id} ({task.short_body}) removed.")


if __name__ == "__main__":
    app()
