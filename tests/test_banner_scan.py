import asyncio
import pytest

from scanner.scans.banner_scan import BannerScanner
from scanner.core.task_context import TaskContext
from scanner.constants import PortState

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
        result = await scanner.scan(
            TaskContext(
                factory=scanner.scan,
                host="127.0.0.1",
                port=port,
                scan_type="banner",
            )
        )

        # Assert
        assert result.state is PortState.OPEN
        # assert result.banner == "SSH-2.0-TestServer"
        # assert result.data == "TEST BANNER"
        # assert result.host == "127.0.0.1"
        # assert result.port == port
        # assert result.scan_type == "banner"

    finally:
        server.close()
        await server.wait_closed()


@pytest.mark.asyncio
async def test_closed_port():

    # Arrange
    scanner = BannerScanner()

    # Act
    result = await scanner.scan(
        TaskContext(
            factory=scanner.scan,
            host="127.0.0.1",
            port=65000,
            scan_type="banner",
        )
    )

    # Assert
    assert result.state in {PortState.CLOSED, PortState.FILTERED}
    # assert result.data is None
    # assert result.host == "127.0.0.1"
    # assert result.port == 65000
    # assert result.scan_type == "banner"
    # assert "Connect call failed" in result.error

@pytest.mark.skip(reason="multi-port orchestration moved to AsyncRunner")
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
        # assert len(results) == 2

        results_by_port = {
            result.port: result
            for result in results
        }

        # assert results_by_port[port].success is True
        # assert results_by_port[port].data == "TEST BANNER"

        # assert results_by_port[65000].success is False
        # assert results_by_port[65000].data is None

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
        result = await scanner.scan(
            TaskContext(
                factory=scanner.scan,
                host="127.0.0.1",
                port=port,
                scan_type="banner",
            )
        )

        # Assert
        assert result.state is PortState.OPEN
        # assert result.banner == ""
        # assert result.data == ""
        # assert result.host == "127.0.0.1"
        # assert result.port == port
        # assert result.scan_type == "banner"

    finally:
        server.close()
        await server.wait_closed()