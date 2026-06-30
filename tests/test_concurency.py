import asyncio
import time
import pytest
from scanner.async_runner import AsyncRunner, TaskContext


async def slow_task():
    await asyncio.sleep(1)
    return "OK"


@pytest.mark.asyncio
async def test_concurrency():

    # Arrange
    runner = AsyncRunner(
        limit=3
    )

    contexts = [
        TaskContext(
            factory=lambda context: slow_task(),
            host="127.0.0.1",
            port=80,
            scan_type="connect"
        )
        for _ in range(3)
    ]

    start = time.perf_counter()

    # Act
    results = await runner.run(contexts)

    elapsed = time.perf_counter() - start

    # Assert
    assert len(results) == 3

    assert all(result.success for result in results)

    # Sequential execution would take about 3 seconds.
    # Concurrent execution should finish much faster.
    assert elapsed < 2