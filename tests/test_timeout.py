import asyncio
import pytest
from scanner.async_runner import AsyncRunner, TaskContext


async def slow_task():
    await asyncio.sleep(2)
    return "OK"


@pytest.mark.asyncio
async def test_timeout():

    # Arrange
    runner = AsyncRunner(timeout=1, retries=0)

    context = TaskContext(
        factory=lambda context: slow_task(),
        host="127.0.0.1",
        port=80,
        scan_type="connect"
    )

    # Act
    results = await runner.run([context])

    # Assert
    assert len(results) == 1

    result = results[0]

    assert result.success is False
    assert result.data is None
    assert result.attempt == 1
    assert result.error == "TimeoutError"