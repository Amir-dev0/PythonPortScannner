from dataclasses import dataclass
from typing import Callable


@dataclass
class TaskContext:
    """
    Describe a task and its execution metadata.
    """

    factory: Callable

    host: str

    scan_type: str

    port: int | None = None
    ports: list[int] | None = None