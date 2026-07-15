from scanner.protocols.base import BaseProtocol


class SSHProtocol(BaseProtocol):

    async def grab_banner(
        self,
        context,
        reader,
        writer,
    ):

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()