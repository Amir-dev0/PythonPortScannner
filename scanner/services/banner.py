import asyncio


HTTP_PORTS = {80, 8080, 8000, 8888}


async def grab_banner(ip, port):

    writer = None

    try:
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(ip, port),
            timeout=2
        )

        try:
            data = await asyncio.wait_for(
                reader.read(1024),
                timeout=1
            )

            if data:
                return data.decode(errors="ignore").strip()

        except asyncio.TimeoutError:
            pass

        if port in HTTP_PORTS:

            request = (
                f"HEAD / HTTP/1.1\r\n"
                f"Host: {ip}\r\n"
                f"Connection: close\r\n\r\n"
            )

            writer.write(request.encode())
            await writer.drain()

            data = await asyncio.wait_for(
                reader.read(4096),
                timeout=2
            )

            return data.decode(errors="ignore")

        return None

    except Exception:
        return None

    finally:
        if writer:
            writer.close()
            await writer.wait_closed()

