from abc import ABC, abstractmethod


class BaseScanner(ABC):

    @abstractmethod
    async def scan(
        self,
        host,
        ports
    ):
        """
        Run scan against target ports.
        """
        raise NotImplementedError