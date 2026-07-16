from scanner.protocols.base import BaseProtocol


class SMTPProtocol(BaseProtocol):
    """
    SMTP banner grabber.

    Reads the SMTP server greeting banner after the TCP connection
    is established.
    """

    async def grab_banner(
        self,
        context,
        reader,
        writer,
    ):

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()