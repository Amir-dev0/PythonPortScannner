from scanner.protocols.base import BaseProtocol


class HTTPProtocol(BaseProtocol):
    """
    HTTP banner grabber.

    Sends a minimal HTTP request to the target service and returns
    the response headers as the banner.
    """

    async def grab_banner(
        self,
        context,
        reader,
        writer,
    ) -> str:

        request = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {context.host}\r\n"
            "Connection: close\r\n"
            "User-Agent: PythonPortScanner\r\n"
            "\r\n"
        )

        writer.write(request.encode())
        await writer.drain()

        await writer.drain()

        banner = await reader.read(1024)

        response = banner.decode(errors="ignore")

        headers = response.split("\r\n\r\n", 1)[0]
        headers = headers.split("\n\n", 1)[0]

        return headers.strip()