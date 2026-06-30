import pytest

from scanner.async_runner import AsyncRunner, TaskContext


calls = {
    "count": 0
}


async def flaky_task():
    calls["count"] += 1

    if calls["count"] == 1:
        raise ConnectionResetError("Temporary Error")

    return "OK"


@pytest.mark.asyncio
async def test_retry():

    # Arrange
    runner = AsyncRunner(retries=1)

    context = TaskContext(
        factory=lambda context: flaky_task(),
        host="127.0.0.1",
        port=80,
        scan_type="connect"
    )

    # Act
    results = await runner.run([context])
 
    # Assert
    assert len(results) == 1

    result = results[0]

    assert result.success is True
    assert result.data == "OK"
    assert result.attempt == 2

    # The task should have been executed twice
    assert calls["count"] == 2
  