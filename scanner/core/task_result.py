from dataclasses import dataclass
from typing import Any, Optional, Callable


@dataclass
class TaskResult():

    """
    Store the outcome of a completed task.
    """

    success: bool
    data: Any = None
    error: Optional[str] = None
    attempt: int = 1

    host: Optional[str] = None
    port: Optional[int] = None
    scan_type: Optional[str] = None
