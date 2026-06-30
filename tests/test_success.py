import pytest

from scanner.async_runner import AsyncRunner, TaskContext


async def fake_task():
    return "OK"


@pytest.mark.asyncio
async def test_success():
    # Arrange
    runner = AsyncRunner()

    context = TaskContext(
        factory=lambda context: fake_task(),
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
    assert result.attempt == 1