import asyncio
import pytest

from scanner.scans.banner_scan import BannerScanner


async def banner_server(reader, writer):
    """
    Test server that immediately sends a banner after a client connects.
    """

    writer.write(b"TEST BANNER\r\n")
    await writer.drain()

    writer.close()
    await writer.wait_closed()


async def empty_banner_server(reader, writer):
    """
    Test server that accepts a connection without sending any data.
    """

    writer.close()
    await writer.wait_closed()


@pytest.mark.asyncio
async def test_banner_scan():

    # Arrange
    server = await asyncio.start_server(
        banner_server,
        "127.0.0.1",
        0
    )

    port = server.sockets[0].getsockname()[1]

    scanner = BannerScanner()

    try:
        # Act
        results = await scanner.scan(
            host="127.0.0.1",
            ports=port
        )

        # Assert
        assert len(results) == 1

        result = results[0]

        assert result.success is True
        assert result.data == "TEST BANNER"
        assert result.host == "127.0.0.1"
        assert result.port == port
        assert result.scan_type == "banner"

    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_closed_port():

    # Arrange
    scanner = BannerScanner()

    # Act
    results = await scanner.scan(
        host="127.0.0.1",
        ports=65000
    )

    # Assert
    assert len(results) == 1

    result = results[0]

    assert result.success is False
    assert result.data is None
    assert result.host == "127.0.0.1"
    assert result.port == 65000
    assert result.scan_type == "banner"
    assert "Connect call failed" in result.error


@pytest.mark.asyncio
async def test_multiple_ports():

    # Arrange
    server = await asyncio.start_server(
        banner_server,
        "127.0.0.1",
        0
    )

    port = server.sockets[0].getsockname()[1]

    scanner = BannerScanner()

    try:
        # Act
        results = await scanner.scan(
            host="127.0.0.1",
            ports=[port, 65000]
        )

        # Assert
        assert len(results) == 2

        results_by_port = {
            result.port: result
            for result in results
        }

        assert results_by_port[port].success is True
        assert results_by_port[port].data == "TEST BANNER"

        assert results_by_port[65000].success is False
        assert results_by_port[65000].data is None

    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_empty_banner():

    # Arrange
    server = await asyncio.start_server(
        empty_banner_server,
        "127.0.0.1",
        0
    )

    port = server.sockets[0].getsockname()[1]

    scanner = BannerScanner()

    try:
        # Act
        results = await scanner.scan(
            host="127.0.0.1",
            ports=port
        )

        # Assert
        assert len(results) == 1

        result = results[0]

        assert result.success is True
        assert result.data == ""
        assert result.host == "127.0.0.1"
        assert result.port == port
        assert result.scan_type == "banner"

    finally:
        server.close()
        await server.wait_closed()