import asyncio
from scanner.cli.parser import CLIParser
from scanner.factory.scanner_factory import ScannerFactory
from scanner.parser.port_parser import PortParser
from scanner.cli.formatter import ResultFormatter
from scanner.parser.host_parser import HostParser

class CLI:

    def __init__(self):

        self._parser = CLIParser()
        self._host_parser = HostParser()

    async def run(self):

        args = self._parser.parse()

        scanner = ScannerFactory.create(
            scan_type=args.scan_type,
            timeout=args.timeout,
            concurrency=args.concurrency,
        )

        port_parser = PortParser()

        ports = port_parser.parse(
            args.ports
        )

        hosts = self._host_parser.parse(
            args.host
        )

        for host in hosts:

            results = await scanner.scan(
                host=host,
                ports=ports,
            )

            ResultFormatter.print(results)