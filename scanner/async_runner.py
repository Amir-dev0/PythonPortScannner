import asyncio

class AsyncRunner():

    def __init__(self, limit: int = 500, timeout: int = 3):
        self.limit = limit
        self.timeout = timeout
        self.semaphore = asyncio.Semaphore(self.limit)
        self.stats = {
            "total": 0,
            "success": 0,
            "error": 0,
            "timeout": 0
        }

    async def _worker(self, coroutine):
        async with self.semaphore:
            try:
                result = await asyncio.wait_for(
                    coroutine,
                    timeout=self.timeout
                )

                self.stats ["success"] += 1
                
                return {
                    "success": True,
                    "data": result,
                    "error": None
                }
            
            except asyncio.TimeoutError:
                self.stats["timeout"] += 1

                return {
                    "success": False,
                    "data": None,
                    "error": "timeout"
                }
            
            except Exception as e:
                self.stats["error"] += 1

                return {
                    "success": False,
                    "data": None,
                    "error": str(e)
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