import re
from scanner.models.scan_info import ScanInfo


class ServiceDetector:
    """
    Detect service name, product and version from banners.
    """

    @staticmethod
    def detect(scan_info: ScanInfo) -> ScanInfo:

        if not scan_info.banner:
            return scan_info

        banner = scan_info.banner

        detectors = (
            ServiceDetector._detect_ssh,
            ServiceDetector._detect_http,
            ServiceDetector._detect_ftp,
            ServiceDetector._detect_smtp,
            ServiceDetector._detect_redis,
            ServiceDetector._detect_mysql,
            ServiceDetector._detect_postgresql,
        )

        for detector in detectors:

            detector(scan_info, banner)

            if scan_info.service:
                break

        return scan_info

    @staticmethod
    def _detect_ssh(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        match = re.search(
            r"OpenSSH[_ ]([^\s]+)",
            banner,
        )

        if match:

            scan_info.service = "ssh"
            scan_info.product = "OpenSSH"
            scan_info.version = match.group(1)

    @staticmethod
    def _detect_http(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        nginx = re.search(
            r"Server:\s*nginx/?([^\r\n ]*)",
            banner,
            re.IGNORECASE,
        )

        if nginx:

            scan_info.service = "http"
            scan_info.product = "nginx"

            if nginx.group(1):
                scan_info.version = nginx.group(1)

            return

        apache = re.search(
            r"Server:\s*Apache/?([^\r\n ]*)",
            banner,
            re.IGNORECASE,
        )

        if apache:

            scan_info.service = "http"
            scan_info.product = "Apache"

            if apache.group(1):
                scan_info.version = apache.group(1)

            return

        if "HTTP/" in banner:

            scan_info.service = "http"

    @staticmethod
    def _detect_ftp(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        if "FTP" in banner.upper():

            scan_info.service = "ftp"

    @staticmethod
    def _detect_smtp(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        if "SMTP" in banner.upper():

            scan_info.service = "smtp"

    @staticmethod
    def _detect_redis(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        match = re.search(
            r"redis_version:([^\r\n ]+)",
            banner,
            re.IGNORECASE,
        )

        if match:

            scan_info.service = "redis"
            scan_info.product = "Redis"
            scan_info.version = match.group(1)

    @staticmethod
    def _detect_mysql(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        match = re.search(
            r"MySQL(?: Community Server)?\s*v?([0-9.]+)",
            banner,
            re.IGNORECASE,
        )

        if match:

            scan_info.service = "mysql"
            scan_info.product = "MySQL"
            scan_info.version = match.group(1)

    @staticmethod
    def _detect_postgresql(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

        match = re.search(
            r"PostgreSQL\s+([0-9.]+)",
            banner,
            re.IGNORECASE,
        )

        if match:

            scan_info.service = "postgresql"
            scan_info.product = "PostgreSQL"
            scan_info.version = match.group(1)