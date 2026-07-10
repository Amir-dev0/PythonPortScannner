import asyncio
from scanner.async_runner import AsyncRunner, TaskContext
from scanner.constants import PortState
from scanner.core.base_scanner import BaseScanner
class ConnectScanner(BaseScanner):

    def __init__(self):
        self.runner = AsyncRunner()

    async def scan(self, host, ports):

        if isinstance(ports, int):
            ports = [ports]
        
        contexts = []

        for port in ports:
            contexts.append(
                TaskContext(
                    factory=self._connect_scan,
                    host=host,
                    port=port,
                    scan_type="connect"
                )
            )

        return await self.runner.run(contexts)    

    async def _connect_scan(self, context):

        try:
            reader, writer = await asyncio.open_connection(
                context.host,
                context.port
            )

            writer.close()
            await writer.wait_closed()

            return PortState.OPEN

        except ConnectionRefusedError:
            return PortState.CLOSED

        except asyncio.TimeoutError:
            return PortState.FILTERED
