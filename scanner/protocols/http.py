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

        response = banner.decode(errors="ignore")

        headers = response.split("\r\n\r\n", 1)[0]
        headers = headers.split("\n\n", 1)[0]

        return headers.strip()