import asyncio
import random
from dataclasses import dataclass
from typing import Any, Optional, Callable
class AsyncRunner():

    def __init__(self, limit: int = 500, timeout: int = 3, retries: int = 2, backoff: bool = True):
        self.limit = limit
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.semaphore = asyncio.Semaphore(self.limit)
        self.stats = {
            "total": 0,
            "success": 0,
            "error": 0,
            "timeout": 0
        }

    async def _worker(self, context: TaskContext):
        async with self.semaphore:
            last_error = None

            for attempt in range(self.retries + 1):
                try:
                    coroutine = context.factory(context)
                    
                    result = await asyncio.wait_for(
                        coroutine,
                        timeout=self.timeout
                    )

                    self.stats ["success"] += 1
                    
                    return TaskResult(
                        success=True,
                        data=result,
                        error=None,
                        attempt=attempt + 1,
                        host=context.host,
                        port=context.port,
                        scan_type=context.scan_type        
                    )

                except Exception as e:
                    last_error = e

                    if not self.should_retry(e):
                        self.stats["error"] += 1
    
                        return TaskResult(
                            success=False,
                            data=None,
                            error=str(e),
                            attempt=attempt + 1,
                            host=context.host,
                            port=context.port,
                            scan_type=context.scan_type
                        )
                    
                    if self.backoff and attempt < self.retries:
                        delay = self.get_retry_delay(attempt)
                        await asyncio.sleep(delay)

            self.stats["error"] += 1
            
            return TaskResult(
                success=False,
                data=None,
                error=str(last_error),
                attempt= self.retries + 1
            )
        
    async def run(self, coroutines):
        self.stats = {
            "total": len(coroutines),
            "success": 0,
            "error": 0,
            "timeout": 0
        }

        tasks = [
            self._worker(coro)
            for coro in coroutines
        ]

        results = await asyncio.gather(*tasks)

        return self.build_scan_report(results)

    def should_retry (self, error: Exception):
        retry_errors = (
            asyncio.TimeoutError,
            ConnectionResetError,
            ConnectionRefusedError,
        )

        return isinstance(error, retry_errors)

    def get_retry_delay(self, attempt: int) -> float:
        max_delay = 2 ** attempt
        return random.uniform(0, max_delay)
    
    def get_stats(self):
        return self.stats.copy()

    def aggregate_results(self, results):
        success = []
        failed = []

        for r in results:
            if r.success:
                success.append(r)
            else:
                failed.append(r)

        return {
            "success": success,
            "failed": failed,
            "total": len(results),
            "success_count": len(success),
            "error_count": len(failed),
        }        

    def build_scan_report(self, results):
        report = {}

        for r in results:

            host = r.host or "unknown"

            if host  not in report:
                report[host] = {
                    "open": [],
                    "closed": []
                }

            if r.success:
                report[host]["open"].append(r.port)
            else:
                report[host]["closed"].append(r.port)

        return report                
@dataclass
class TaskResult():
    success: bool
    data: Any = None
    error: Optional[str] = None
    attempt: int = 1

    host: Optional[str] = None
    port: Optional[str] = None
    scan_type: Optional[str] = None

@dataclass
class TaskContext():
    factory: Callable
    host: str
    port: int
    scan_type: str