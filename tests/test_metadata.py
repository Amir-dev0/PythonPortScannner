import pytest
from scanner.async_runner import AsyncRunner, TaskContext


async def fake_task():
    return "OK"


@pytest.mark.asyncio
async def test_metadata():

    # Arrange
    runner = AsyncRunner()

    context = TaskContext(
        factory=lambda context: fake_task(),
        host="192.168.1.50",
        port=443,
        scan_type="connect"
    )

    # Act
    results = await runner.run([context])

    # Assert
    result = results[0]

    assert result.host == "192.168.1.50"
    assert result.port == 443
    assert result.scan_type == "connect"