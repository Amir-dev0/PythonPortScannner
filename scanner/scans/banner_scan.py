import asyncio
from scanner.async_runner import AsyncRunner, TaskContext
from scanner.core.base_scanner import BaseScanner
from scanner.models.scan_info import ScanInfo
from scanner.constants import PortState
from scanner.detection.service_detector import ServiceDetector

class BannerScanner(BaseScanner):

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

            scan_info = ScanInfo(
                state=PortState.OPEN,
                banner=banner.decode(errors="ignore").strip(),
            )

            ServiceDetector.detect(scan_info)

            return scan_info

        finally:
            writer.close()
            await writer.wait_closed()