from scanner.protocols.base import BaseProtocol


class GenericProtocol(BaseProtocol):
    """
    Generic banner grabber.

    Waits for data from the remote service without applying any
    protocol-specific communication.
    """

    async def grab_banner(
        self,
        context,
        reader,
        writer,
    ) -> str:

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()