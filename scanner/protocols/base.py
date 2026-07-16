from abc import ABC, abstractmethod


class BaseProtocol(ABC):
    """
    Abstract base class for protocol-specific banner grabbing.

    Each protocol implementation defines how to communicate with a
    service and retrieve its banner.
    """
    
    @abstractmethod
    async def grab_banner(
        self,
        reader,
        writer,
    ) -> str:
        ...