from abc import ABC, abstractmethod
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TaskProgressColumn,
    TextColumn,
    TimeElapsedColumn,
)


class ProgressReporter(ABC):
    """
    Base interface for reporting scan progress.
    """

    @abstractmethod
    def start(self, total: int) -> None:
        """
        Initialize progress reporting.
        """
        ...

    @abstractmethod
    def advance(self, step: int = 1) -> None:
        """
        Advance the progress by the given number of completed tasks.
        """
        ...

    @abstractmethod
    def finish(self) -> None:
        """
        Finalize progress reporting.
        """
        ...


class NullProgressReporter(ProgressReporter):
    """
    Default progress reporter that performs no action.
    """

    def start(self, total: int) -> None:
        return None

    def advance(self, step: int = 1) -> None:
        return None

    def finish(self) -> None:
        return None


class RichProgressReporter(ProgressReporter):
    """
    Rich-based progress reporter for CLI scans.
    """

    def __init__(self) -> None:

        self.progress = Progress(
            SpinnerColumn(),
            TextColumn("[bold cyan]Scanning"),
            BarColumn(),
            TaskProgressColumn(),
            TimeElapsedColumn(),
        )

        self.task_id: int | None = None

    def start(self, total: int) -> None:

        self.progress.start()

        self.task_id = self.progress.add_task(
            description="Scanning",
            total=total,
        )

    def advance(self, step: int = 1) -> None:

        if self.task_id is not None:

            self.progress.advance(
                self.task_id,
                advance=step,
            )

    def finish(self) -> None:

        self.progress.stop()