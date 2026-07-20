import pytest
from scanner.scans.connect_scan import ConnectScanner
from scanner.core.task_context import TaskContext
from scanner.constants import PortState
"""
Test requirements:

Run a local HTTP server before executing these tests:

    python -m http.server 8080
"""

@pytest.mark.asyncio
async def test_open_port():

    # Arrange
    scanner = ConnectScanner()

    # Act
    result = await scanner.scan(
        TaskContext(
            factory=scanner.scan,
            host="127.0.0.1",
            port=8080,
            scan_type="connect",
        )
    )

    # Assert
    assert result.state is PortState.OPEN
    # assert result.data == "Open"
    # assert result.host == "127.0.0.1"
    # assert result.port == 8080
    # assert result.scan_type == "connect"

@pytest.mark.asyncio
async def test_closed_connect():

    # Arrange
    scanner = ConnectScanner()

    # Act
    result = await scanner.scan(
        TaskContext(
            factory=scanner.scan,
            host="127.0.0.1",
            port=22,
            scan_type="connect",
        )
    )

    # Assert

    print(result)
    assert result.state is PortState.CLOSED
    # assert result.host == "127.0.0.1"
    # assert result.port == 22
    # assert result.scan_type == "connect"
    # assert "Connect call failed" in result.error

@pytest.mark.skip(reason="multi-port orchestration moved to AsyncRunner")
@pytest.mark.asyncio
async def test_multiple_ports():

    # Arrange
    scanner = ConnectScanner()

    # Act
    results = await scanner.scan(host="127.0.0.1", ports=[8000, 8080])

    # Assert
    assert len(results) == 2

    results_by_port = {
        result.port: result
        for result in results
    }

    # assert results_by_port[8080].success is True
    # assert results_by_port[8000].success is False