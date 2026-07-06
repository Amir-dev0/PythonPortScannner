import argparse


class CLIParser:
    """
    Build and parse command-line arguments.
    """

    def __init__(self) -> None:

        self._parser = argparse.ArgumentParser(
            prog="PythonPortScanner",
            description="Modern asynchronous port scanner written in Python."
        )

        self._register_arguments()

    def _register_arguments(self) -> None:
        """
        Register all command-line arguments.
        """

        self._parser.add_argument(
            "host",
            help="Target host or IP address."
        )

        self._parser.add_argument(
            "-p",
            "--ports",
            default="80",
            help="Ports to scan (e.g. 22,80,443)."
        )

    def parse(self) -> argparse.Namespace:
        """
        Parse command-line arguments.
        """

        return self._parser.parse_args()