from abc import ABC, abstractmethod
from scanner.core.task_context import TaskContext
from scanner.models.scan_info import ScanInfo
class BaseScanner(ABC):

    @abstractmethod
    async def scan(
        self,
        context: TaskContext,
    ) -> ScanInfo:
        """
        Run scan against target ports.
        """
        raise NotImplementedError