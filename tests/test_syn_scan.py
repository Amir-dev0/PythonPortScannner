import pytest
import os
from scanner.scans.syn_scan import SynScanner

requires_root = pytest.mark.skipif(
    os.geteuid() != 0,
    reason="Requires CAP_NET_RAW or root privileges"
)

@pytest.fixture
def scanner():
    return SynScanner()


# -----------------------------
# Packet Builder
# -----------------------------

def test_build_packet(scanner):

    packet = scanner._build_packet(
        source_ip="192.168.1.100",
        destination_ip="8.8.8.8",
        source_port=50000,
        destination_port=80
    )

    assert isinstance(packet, bytes)
    assert len(packet) == 20


# -----------------------------
# Checksum
# -----------------------------

def test_calculate_checksum(scanner):

    checksum = scanner._calculate_checksum(
        b"hello world"
    )

    assert isinstance(checksum, int)
    assert 0 <= checksum <= 0xFFFF


# -----------------------------
# Pseudo Header
# -----------------------------

def test_build_pseudo_header(scanner):

    pseudo = scanner._build_pseudo_header(
        "192.168.1.100",
        "8.8.8.8",
        20
    )

    assert isinstance(pseudo, bytes)
    assert len(pseudo) == 12


# -----------------------------
# Source Port
# -----------------------------

def test_generate_source_port(scanner):

    port = scanner._generate_source_port()

    assert 49152 <= port <= 65535


# -----------------------------
# Parse Response
# -----------------------------

def test_parse_response_open(scanner):

    packet = (
        b"\x45\x00\x00\x28"
        b"\x00\x00\x00\x00"
        b"\x40\x06\x00\x00"
        b"\x08\x08\x08\x08"
        b"\xc0\xa8\x01\x64"
        b"\x00\x50"
        b"\xc3\x50"
        b"\x00\x00\x00\x00"
        b"\x00\x00\x00\x00"
        b"\x50"
        b"\x12"
        b"\x00\x00"
        b"\x00\x00"
        b"\x00\x00"
    )

    assert scanner._parse_response(packet) == "Open"


def test_parse_response_closed(scanner):

    packet = (
        b"\x45\x00\x00\x28"
        b"\x00\x00\x00\x00"
        b"\x40\x06\x00\x00"
        b"\x08\x08\x08\x08"
        b"\xc0\xa8\x01\x64"
        b"\x00\x50"
        b"\xc3\x50"
        b"\x00\x00\x00\x00"
        b"\x00\x00\x00\x00"
        b"\x50"
        b"\x14"
        b"\x00\x00"
        b"\x00\x00"
        b"\x00\x00"
    )

    assert scanner._parse_response(packet) == "Closed"


# -----------------------------
# Integration Tests
# -----------------------------

@requires_root
@pytest.mark.asyncio
async def test_syn_scan_open(scanner):

    results = await scanner.scan(
        host="scanme.nmap.org",
        ports=80
    )

    assert len(results) == 1
    assert results[0].success is True
    assert results[0].data == "Open"


@requires_root
@pytest.mark.asyncio
async def test_syn_scan_closed(scanner):

    results = await scanner.scan(
        host="scanme.nmap.org",
        ports=81
    )

    assert len(results) == 1
    assert results[0].success is True
    assert results[0].data == "Closed"


@pytest.mark.asyncio
async def test_multiple_ports(scanner):

    results = await scanner.scan(
        host="scanme.nmap.org",
        ports=[80, 81]
    )

    assert len(results) == 2