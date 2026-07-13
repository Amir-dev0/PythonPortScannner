from dataclasses import dataclass

from scanner.constants import PortState


@dataclass(slots=True)
class ScanInfo:
    """
    Represents the information collected from a scanned port.
    """

    state: PortState

    banner: str | None = None

    service: str | None = None

    version: str | None = None