import asyncio

from scanner.constants import PortState
from scanner.core.base_scanner import BaseScanner
from scanner.core.task_context import TaskContext
from scanner.models.scan_info import ScanInfo
from scanner.detection.service_detector import ServiceDetector
from scanner.protocols.factory import ProtocolFactory


class BannerScanner(BaseScanner):

    async def scan(
        self,
        context: TaskContext,
    ) -> ScanInfo:

        reader, writer = await asyncio.open_connection(
            context.host,
            context.port,
        )

        try:
            protocol = ProtocolFactory.create(
                context.port
            )

            banner = await protocol.grab_banner(
                context,
                reader,
                writer,
            )

            scan_info = ScanInfo(
                endpoint=f"{context.host}:{context.port}",
                state=PortState.OPEN,
                banner=banner,
            )

            ServiceDetector.detect(scan_info)

            return scan_info

        finally:
            writer.close()
            await writer.wait_closed()