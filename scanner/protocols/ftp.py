from scanner.protocols.base import BaseProtocol


class FTPProtocol(BaseProtocol):

    async def grab_banner(
        self,
        reader,
        writer,
    ) -> str:

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()