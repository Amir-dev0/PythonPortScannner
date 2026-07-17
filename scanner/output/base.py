from abc import ABC, abstractmethod
from scanner.models.scan_info import ScanInfo


class OutputWriter(ABC):

    @abstractmethod
    def write(
        self,
        results: list[ScanInfo],
        output: str,
    ) -> None:
        ...