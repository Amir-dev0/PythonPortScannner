import asyncio
from scanner.async_runner import AsyncRunner, TaskContext
from scanner.constants import PortState
from scanner.core.base_scanner import BaseScanner
from scanner.models.scan_info import ScanInfo
class ConnectScanner(BaseScanner):

    def __init__(
        self,
        timeout: float = 3,
        concurrency: int = 500,
    ) -> None:

        self.runner = AsyncRunner(
            timeout=timeout,
            limit=concurrency,
        )
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

            return ScanInfo(
                state=PortState.OPEN
            )

        except ConnectionRefusedError:
            return ScanInfo(
                state=PortState.CLOSED
                ) 

        except asyncio.TimeoutError:
            return ScanInfo(
                state=PortState.FILTERED
            )
            
