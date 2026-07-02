import asyncio
from scanner.async_runner import AsyncRunner, TaskContext


class BannerScanner:

    def __init__(self):

        self.runner = AsyncRunner()

    async def scan(self, host, ports):

        # Allow scanning a single port or multiple ports
        if isinstance(ports, int):
            ports = [ports]

        contexts =[]

        for port in ports:
            contexts.append(
                TaskContext(
                    factory=self._banner_scan,
                    host=host,
                    port=port,
                    scan_type="banner"
                )
            )
        
        return await self.runner.run(contexts)
    async def _banner_scan(self, context):

        reader, writer = await asyncio.open_connection(
            context.host,
            context.port
        )

        try:
            banner = await reader.read(1024)

            return banner.decode(errors="ignore").strip()
        
        finally:
            writer.close()
            await writer.wait_closed()