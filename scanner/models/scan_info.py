from dataclasses import dataclass

from scanner.constants import PortState


@dataclass(slots=True)
class ScanInfo:
    """
    Unified result model returned by all scanners.
    """

    endpoint: str

    state: PortState

    banner: str | None = None

    service: str | None = None

    product: str | None = None

    version: str | None = None

    latency: float | None = None