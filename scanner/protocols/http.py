from scanner.protocols.base import BaseProtocol


class HTTPProtocol(BaseProtocol):

    async def grab_banner(
        self,
        reader,
        writer,
    ) -> str:

        writer.write(
            b"GET / HTTP/1.0\r\n\r\n"
        )

        await writer.drain()

        banner = await reader.read(1024)

        return banner.decode(errors="ignore").strip()