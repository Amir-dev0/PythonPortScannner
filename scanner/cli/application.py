import asyncio

from scanner.cli.parser import CLIParser
from scanner.factory.scanner_factory import ScannerFactory


class CLI:

    def __init__(self):

        self._parser = CLIParser()

    async def run(self):

        args = self._parser.parse()

        scanner = ScannerFactory.create(args.scan_type)

        results = await scanner.scan(
            host=args.host,
            ports=[80]
        )

        for result in results:
            print(
                f"{result.host}:{result.port} -> {result.data.value}"
            )