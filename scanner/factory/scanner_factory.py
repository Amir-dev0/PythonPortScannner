from scanner.scans.connect_scan import ConnectScanner
from scanner.scans.syn_scan import SynScanner
from scanner.scans.banner_scan import BannerScanner
from scanner.core.base_scanner import BaseScanner

class ScannerFactory:

    @staticmethod
    def create(
        scan_type: str,
        timeout: float = 3,
        concurrency: int = 500,
    ) -> BaseScanner:

        scanners = {
            "connect": ConnectScanner,
            "syn": SynScanner,
            "banner": BannerScanner,
        }

        try:
            scanner_class = scanners[scan_type]

        except KeyError:
            raise ValueError(
                f"Unknown scan type: {scan_type}"
            )

        return scanner_class(
            timeout=timeout,
            concurrency=concurrency,
        )