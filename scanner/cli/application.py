import asyncio
from scanner.cli.parser import CLIParser
from scanner.factory.scanner_factory import ScannerFactory
from scanner.parser.port_parser import PortParser


class CLI:

    def __init__(self):

        self._parser = CLIParser()

    async def run(self):

        args = self._parser.parse()

        scanner = ScannerFactory.create(args.scan_type)

        parser = PortParser()

        ports = parser.parse(
            args.ports
        )

        results = await scanner.scan(
            host=args.host,
            ports=ports
        )

        for result in results:

            if result.success:
                print(
                    f"{result.host}:{result.port} -> {result.data.value}"
                )
            else:
                print(
                    f"{result.host}:{result.port} -> ERROR ({result.error})"
                )
