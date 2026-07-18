import asyncio
import random
from scanner.core.task_context import TaskContext
from scanner.core.task_result import TaskResult
from scanner.cli.progress import ProgressReporter,NullProgressReporter
class AsyncRunner:
    
    """
    Execute asynchronous tasks with concurrency control,
    timeout handling and retry support.
    """

    def __init__(
        self,
        timeout: float = 3,
        limit: int = 500,
        retries: int = 2,
        backoff: bool = True,
        reporter: ProgressReporter | None = None,
    ) -> None:
        
        self.limit = limit
        self.timeout = timeout
        self.retries = retries
        self.backoff = backoff
        self.reporter = reporter or NullProgressReporter()
        self.semaphore = asyncio.Semaphore(self.limit)
        self.stats = {
            "total": 0,
            "success": 0,
            "error": 0,
            "timeout": 0
        }

    async def _worker(self, context: TaskContext) -> TaskResult:
        """
        Execute a single task with retry, timeout and concurrency control.
        """

        async with self.semaphore:
            last_error = None

            for attempt in range(self.retries + 1):
                try:
                    # Create a fresh coroutine for every retry attempt
                    coroutine = context.factory(context)

                    # Execute with timeout
                    result = await asyncio.wait_for(
                        coroutine,
                        timeout=self.timeout
                    )

                    self.stats["success"] += 1

                    self.reporter.advance()

                    return TaskResult(
                        success=True,
                        data=result,
                        error=None,
                        attempt=attempt + 1,
                        host=context.host,
                        port=context.port,
                        scan_type=context.scan_type
                    )

                except asyncio.TimeoutError as e:
                    last_error = e

                except Exception as e:
                    last_error = e

                    # Stop immediately for non-retryable errors
                    if not self.should_retry(e):
                        break

                # Wait before the next retry (if enabled)
                if self.backoff and attempt < self.retries:
                    delay = self.get_retry_delay(attempt)
                    await asyncio.sleep(delay)

            # Update statistics only once after all attempts have finished
            if isinstance(last_error, asyncio.TimeoutError):
                self.stats["timeout"] += 1
            else:
                self.stats["error"] += 1

            if isinstance(last_error, asyncio.TimeoutError):
                error_message = "TimeoutError"
            else:
                error_message = str(last_error)   
            
            self.reporter.advance()
            
            return TaskResult(
                success=False,
                data=None,
                error=error_message,
                attempt=attempt + 1,
                host=context.host,
                port=context.port,
                scan_type=context.scan_type
            )
    async def run(self, contexts):

        """
        Execute multiple tasks concurrently and return their results.
        """

        self.stats = {
            "total": len(contexts),
            "success": 0,
            "error": 0,
            "timeout": 0
        }
        self.reporter.start(len(contexts))

        tasks = [
            self._worker(context)
            for context in contexts
        ]

        results = await asyncio.gather(*tasks)

        self.reporter.finish()
        
        return results

    def should_retry (self, error: Exception):

        """
        Return True if the exception should trigger a retry.
        """

        retry_errors = (
            asyncio.TimeoutError,
            ConnectionResetError,
            ConnectionRefusedError,
        )

        return isinstance(error, retry_errors)

    def get_retry_delay(self, attempt: int) -> float:

        """
        Calculate exponential backoff delay with jitter.
        """

        max_delay = 2 ** attempt
        return random.uniform(0, max_delay)
    
    def get_stats(self):

        """
        Return a copy of the current execution statistics.
        """

        return self.stats.copy()