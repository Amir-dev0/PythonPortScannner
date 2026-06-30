import pytest
from scanner.async_runner import AsyncRunner, TaskContext

async def failing_task():
    raise ValueError("Test Error")

@pytest.mark.asyncio
async def test_failure():
    # Arrange
    runner = AsyncRunner(retries=0)

    #Act
    context = TaskContext(
        factory=lambda context: failing_task(),
        host="127.0.0.1",
        port=80,
        scan_type="connect"
    )

    results = await runner.run([context])

    #Assert
    assert len(results) == 1
    result = results[0]

    assert result.success is False
    assert result.data is None
    assert result.attempt == 1
    assert "Test Error" in result.error