from abc import ABC, abstractmethod


class BaseProtocol(ABC):

    @abstractmethod
    async def grab_banner(
        self,
        reader,
        writer,
    ) -> str:
        ...