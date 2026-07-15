from scanner.protocols.base import BaseProtocol


class GenericProtocol(BaseProtocol):

    async def grab_banner(
        self,
        context,
        reader,
        writer,
    ) -> str:

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()