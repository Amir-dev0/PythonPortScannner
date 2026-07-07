from scanner.scans.connect_scan import ConnectScanner
from scanner.scans.syn_scan import SynScanner
from scanner.scans.banner_scan import BannerScanner


class ScannerFactory:

    @staticmethod
    def create(scan_type: str):

        scanners = {
            "connect": ConnectScanner,
            "syn": SynScanner,
            "banner": BannerScanner,
        }

        try:
            return scanners[scan_type]()

        except KeyError:
            raise ValueError(
                f"Unknown scan type: {scan_type}"
            )