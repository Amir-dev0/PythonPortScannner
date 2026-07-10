import pytest
from scanner.parser.port_parser import PortParser


@pytest.fixture
def parser():

    return PortParser()

# test 1
def test_single_port(parser):

    assert parser.parse("80") == [80]

# testy 2
def test_multiple_ports(parser):

    assert parser.parse(
        "22,80,443"
    ) == [22,80,443]

# test 3
def test_port_range(parser):

    assert parser.parse(
        "1-5"
    ) == [1,2,3,4,5]

# test 4
def test_mixed_ports(parser):

    assert parser.parse(
        "22,80,1000-1002"
    ) == [
        22,
        80,
        1000,
        1001,
        1002
    ]

# tset 5
def test_duplicate_ports(parser):

    assert parser.parse(
        "80,22,80"
    ) == [22,80]

# test 6
def test_invalid_port(parser):

    with pytest.raises(ValueError):

        parser.parse("70000")

# test 7
def test_invalid_range(parser):

    with pytest.raises(ValueError):

        parser.parse("100-20")

# test 8
def test_invalid_string(parser):

    with pytest.raises(ValueError):

        parser.parse("abc")                                    