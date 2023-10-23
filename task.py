from datetime import datetime
from typing import TextIO
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, field_validator


class Task(BaseModel):
    body: str
    created_at: datetime = Field(default_factory=datetime.now)
    absolute_id: UUID = Field(default_factory=uuid4)

    def __str__(self) -> str:
        return f"{self.body} ({self.created_at:%d/%m/%Y - %H:%M})"

    @field_validator("body")
    @classmethod
    def body_validator(cls, v: str) -> str:
        v = v.strip()
        return v

    @property
    def short_body(self) -> str:
        if len(self.body) <= 15:
            return self.body

        return f"{self.body[: 15 - 3]}..."


# I couldn't find how to load/dump lists of pydantic models for V2
class _Tasks(BaseModel):
    tasks: list[Task]


def load_tasks(file: TextIO) -> list[Task]:
    return _Tasks.model_validate_json(file.read()).tasks


def save_tasks(file: TextIO, tasks: list[Task]):
    t = _Tasks(tasks=tasks)
    file.write(t.model_dump_json())
