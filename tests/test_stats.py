import asyncio
import pytest

from scanner.async_runner import AsyncRunner, TaskContext


async def success_task():
    return "OK"


async def error_task():
    raise ValueError("Test Error")


async def timeout_task():
    await asyncio.sleep(2)


@pytest.mark.asyncio
async def test_stats():

    # Arrange
    runner = AsyncRunner(timeout=1, retries=0)

    contexts = [
        TaskContext(
            factory=lambda context: success_task(),
            host="127.0.0.1",
            port=80,
            scan_type="connect"
        ),
        TaskContext(
            factory=lambda context: error_task(),
            host="127.0.0.1",
            port=81,
            scan_type="connect"
        ),
        TaskContext(
            factory=lambda context: timeout_task(),
            host="127.0.0.1",
            port=82,
            scan_type="connect"
        ),
    ]

    # Act
    await runner.run(contexts)

    stats = runner.get_stats()

    # Assert
    assert stats["total"] == 3
    assert stats["success"] == 1
    assert stats["error"] == 1
    assert stats["timeout"] == 1