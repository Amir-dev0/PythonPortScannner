from scanner.constants import PortState
from scanner.detection.service_detector import ServiceDetector
from scanner.models.scan_info import ScanInfo


def detect(banner: str) -> ScanInfo:

    scan_info = ScanInfo(
        state=PortState.OPEN,
        banner=banner,
    )

    return ServiceDetector.detect(scan_info)


def test_detect_openssh():

    result = detect(
        "SSH-2.0-OpenSSH_9.8p1 Ubuntu-1ubuntu1"
    )

    assert result.service == "ssh"
    assert result.product == "OpenSSH"
    assert result.version == "9.8p1"


def test_detect_nginx():

    result = detect(
        "HTTP/1.1 200 OK\r\n"
        "Server: nginx/1.26.1\r\n"
    )

    assert result.service == "http"
    assert result.product == "nginx"
    assert result.version == "1.26.1"


def test_detect_apache():

    result = detect(
        "HTTP/1.1 200 OK\r\n"
        "Server: Apache/2.4.62\r\n"
    )

    assert result.service == "http"
    assert result.product == "Apache"
    assert result.version == "2.4.62"


def test_detect_ftp():

    result = detect(
        "220 FTP Server Ready"
    )

    assert result.service == "ftp"
    assert result.product is None
    assert result.version is None


def test_detect_smtp():

    result = detect(
        "220 mail.example.com ESMTP Postfix"
    )

    assert result.service == "smtp"
    assert result.product is None
    assert result.version is None


def test_detect_redis():

    result = detect(
        "redis_version:7.2.4"
    )

    assert result.service == "redis"
    assert result.product == "Redis"
    assert result.version == "7.2.4"


def test_detect_postgresql():

    result = detect(
        "PostgreSQL 16.3"
    )

    assert result.service == "postgresql"
    assert result.product == "PostgreSQL"
    assert result.version == "16.3"


def test_detect_mysql():

    result = detect(
        "MySQL Community Server 8.4.2"
    )

    assert result.service == "mysql"
    assert result.product == "MySQL"
    assert result.version == "8.4.2"


def test_unknown_banner():

    result = detect(
        "Some Random Banner"
    )

    assert result.service is None
    assert result.product is None
    assert result.version is None


def test_empty_banner():

    result = detect("")

    assert result.service is None
    assert result.product is None
    assert result.version is None