import asyncio
from scanner.async_runner import AsyncRunner, TaskContext

class ConnectScanner:

    def __init__(self):
        self.runner = AsyncRunner()

    async def scan(self, host, ports):
        pass

    async def _connect_scan(self, context):
        
        reader, writer = await asyncio.open_connection(
            context.host,
            context.port
        )

        writer.close()
        await writer.wait_closed()

        return "Open"