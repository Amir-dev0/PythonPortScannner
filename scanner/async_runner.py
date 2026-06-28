import asyncio

class AsyncRunner():

    def __init__(self, limit: int = 500, timeout: int = 3, retries: int = 2):
        self.limit = limit
        self.timeout = timeout
        self.retries = retries
        self.semaphore = asyncio.Semaphore(self.limit)
        self.stats = {
            "total": 0,
            "success": 0,
            "error": 0,
            "timeout": 0
        }

    async def _worker(self, coroutine):
        async with self.semaphore:
            last_error = None

            for attempt in range(self.retries + 1):
                try:
                    result = await asyncio.wait_for(
                        coroutine,
                        timeout=self.timeout
                    )

                    self.stats ["success"] += 1
                    
                    return {
                        "success": True,
                        "data": result,
                        "error": None,
                        "attempt": attempt + 1
                    }
                
                except asyncio.TimeoutError:
                    last_error = "timeout"

                except Exception as e:
                    last_error = str(e)

            self.stats["timeout"] += 1    
                    
            return {
                "success": False,
                "data": None,
                "error": last_error,
                "attempt": self.retries + 1
            }
        
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

        return {
            "results": results,
            "stats": self.stats
        }