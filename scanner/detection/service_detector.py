import re

from scanner.models.scan_info import ScanInfo


class ServiceDetector:
    """
    Detect service name and version from banners.
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

        if "OpenSSH" in banner:

            scan_info.service = "ssh"

            match = re.search(
                r"OpenSSH[_ ]([^\s]+)",
                banner,
            )

            if match:
                scan_info.version = match.group(1)

    @staticmethod
    def _detect_http(
        scan_info: ScanInfo,
        banner: str,
    ) -> None:

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