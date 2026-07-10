from dataclasses import dataclass
from typing import Any, Optional, Callable

@dataclass
class TaskContext():

    """
    Describe a task and its execution metadata.
    """

    factory: Callable
    host: str
    port: int
    scan_type: str    