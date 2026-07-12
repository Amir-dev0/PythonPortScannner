from scanner.async_runner import AsyncRunner
from scanner.core.task_context import TaskContext


class HostRunner:

    def __init__(
        self,
        scanner,
        timeout: float = 3,
        concurrency: int = 100,
    ) -> None:

        self.scanner = scanner

        self.runner = AsyncRunner(
            timeout=timeout,
            limit=concurrency,
            retries=0,
        )

    async def run(
        self,
        hosts: list[str],
        ports: list[int],
        scan_type: str,
    ):

        contexts = [
            TaskContext(
                factory=self._scan_host,
                host=host,
                ports=ports,
                scan_type=scan_type,
            )
            for host in hosts
        ]

        return await self.runner.run(contexts)



    async def _scan_host(
        self,
        context: TaskContext,
    ):

        result = await self.scanner.scan(
            host=context.host,
            ports=context.ports,
        )

        return result