import pytest
from scanner.scans.connect_scan import ConnectScanner

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
    results = await scanner.scan(host="127.0.0.1", ports=8080)

    # Assert
    assert len(results) == 1

    result = results[0]

    assert result.success is True
    assert result.data == "Open"
    assert result.host == "127.0.0.1"
    assert result.port == 8080
    assert result.scan_type == "connect"

@pytest.mark.asyncio
async def test_closed_connect():

    # Arrange
    scanner = ConnectScanner()

    # Act
    results = await scanner.scan(host="127.0.0.1", ports=22)

    # Assert
    assert len(results) == 1

    result = results[0]
    print(result)
    assert result.success is False
    assert result.host == "127.0.0.1"
    assert result.port == 22
    assert result.scan_type == "connect"
    assert "Connect call failed" in result.error

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

    assert results_by_port[8080].success is True
    assert results_by_port[8000].success is False