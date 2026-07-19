import asyncio
from scanner.constants import PortState
from scanner.core.base_scanner import BaseScanner
from scanner.core.task_context import TaskContext
from scanner.models.scan_info import ScanInfo


class ConnectScanner(BaseScanner):

    async def scan(
        self,
        context: TaskContext,
    ) -> ScanInfo:

        try:
            reader, writer = await asyncio.open_connection(
                context.host,
                context.port,
            )

            writer.close()
            await writer.wait_closed()

            return ScanInfo(
                endpoint=f"{context.host}:{context.port}",
                state=PortState.OPEN,
            )

        except ConnectionRefusedError:
            return ScanInfo(
                endpoint=f"{context.host}:{context.port}",
                state=PortState.CLOSED,
            )

        except asyncio.TimeoutError:
            return ScanInfo(
                endpoint=f"{context.host}:{context.port}",
                state=PortState.FILTERED,
            )