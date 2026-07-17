import argparse
from pathlib import Path


class CLIParser:
    """
    Build and parse command-line arguments.
    """

    def __init__(self) -> None:
        self._argument_parser = argparse.ArgumentParser(
            prog="PythonPortScanner",
            description="Modern asynchronous port scanner written in Python."
        )
        self._register_arguments()

    def _register_arguments(self) -> None:

        self._argument_parser.add_argument(
            "host",
            help="Target host or IP address."
        )

        self._argument_parser.add_argument(
            "-p", "--ports",
            default="80",
            help="Ports to scan (e.g. 22,80,443)."
        )

        self._argument_parser.add_argument(
            "-s", "--scan-type",
            choices=["connect", "syn", "banner"],
            default="connect",
            help="Scan type to use."
        )

        self._argument_parser.add_argument(
            "--timeout",
            type=float,
            default=3,
            help="Socket timeout in seconds."
        )

        self._argument_parser.add_argument(
            "--concurrency",
            type=int,
            default=500,
            help="Maximum concurrent scan tasks."
        )

        # 👇 این قسمت را اضافه کن
        self._argument_parser.add_argument(
            "-o",
            "--output",
            type=Path,
            metavar="FILE",
            help="Export scan results to a JSON or CSV file."
        )

    def parse(self) -> argparse.Namespace:
        return self._argument_parser.parse_args()