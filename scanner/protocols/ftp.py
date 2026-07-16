from scanner.protocols.base import BaseProtocol


class FTPProtocol(BaseProtocol):
    """
    FTP banner grabber.

    Reads the server greeting banner immediately after establishing
    the connection.
    """

    async def grab_banner(
        self,
        context,
        reader,
        writer,
    ):

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()