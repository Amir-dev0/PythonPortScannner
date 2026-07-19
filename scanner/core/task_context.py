from dataclasses import dataclass
from typing import Callable


@dataclass(slots=True)
class TaskContext:
    """
    Describe a single scan task.
    """

    factory: Callable
    host: str
    port: int
    scan_type: str