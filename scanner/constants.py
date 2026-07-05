from enum import Enum


class PortState(str, Enum):
    OPEN = "Open"
    CLOSED = "Closed"
    FILTERED = "Filtered"
    UNKNOWN = "Unknown"