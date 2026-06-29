import asyncio
import random
from dataclasses import dataclass
from typing import Any, Optional
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

    async def _worker(self, factory):
        async with self.semaphore:
            last_error = None

            for attempt in range(self.retries + 1):
                try:
                    coroutine = factory()
                    
                    result = await asyncio.wait_for(
                        coroutine,
                        timeout=self.timeout
                    )

                    self.stats ["success"] += 1
                    
                    return TaskResult(
                        success=True,
                        data=result,
                        error=None,
                        attempt=attempt + 1
                    )

                except Exception as e:
                    last_error = e

                    if not self.should_retry(e):
                        self.stats["error"] += 1
    
                        return TaskResult(
                            success=False,
                            data=None,
                            error=str(e),
                            attempt=attempt + 1
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

        return results

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

@dataclass
class TaskResult():
    success: bool
    data: Any = None
    error: Optional[str] = None
    attempt: int = 1    