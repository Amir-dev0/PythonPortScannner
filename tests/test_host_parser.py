import pytest

from scanner.parser.host_parser import HostParser


@pytest.fixture
def parser():

    return HostParser()


def test_hostname(parser):

    assert parser.parse(
        "scanme.nmap.org"
    ) == [
        "scanme.nmap.org"
    ]


def test_ipv4(parser):

    assert parser.parse(
        "192.168.1.10"
    ) == [
        "192.168.1.10"
    ]


def test_cidr(parser):

    assert parser.parse(
        "192.168.1.0/30"
    ) == [
        "192.168.1.1",
        "192.168.1.2",
    ]