import asyncio
from scanner.cli.parser import CLIParser
from scanner.factory.scanner_factory import ScannerFactory
from scanner.parser.port_parser import PortParser
from scanner.cli.formatter import ResultFormatter

class CLI:

    def __init__(self):

        self._parser = CLIParser()

    async def run(self):

        args = self._parser.parse()

        scanner = ScannerFactory.create(
            scan_type=args.scan_type,
            timeout=args.timeout,
            concurrency=args.concurrency
        )

        parser = PortParser()

        ports = parser.parse(
            args.ports
        )

        results = await scanner.scan(
            host=args.host,
            ports=ports
        )

        ResultFormatter.print(results)