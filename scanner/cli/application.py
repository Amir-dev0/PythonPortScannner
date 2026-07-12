import asyncio
from scanner.cli.parser import CLIParser
from scanner.factory.scanner_factory import ScannerFactory
from scanner.parser.port_parser import PortParser
from scanner.cli.formatter import ResultFormatter
from scanner.parser.host_parser import HostParser
from scanner.core.host_runner import HostRunner

class CLI:

    def __init__(self):

        self._parser = CLIParser()
        self._host_parser = HostParser()
        self._port_parser = PortParser()

    async def run(self):

        args = self._parser.parse()

        scanner = ScannerFactory.create(
            scan_type=args.scan_type,
            timeout=args.timeout,
            concurrency=args.concurrency,
        )

        port_parser = PortParser()

        hosts = self._host_parser.parse(args.host)

        ports = self._port_parser.parse(args.ports)

        host_runner = HostRunner(
            scanner=scanner,
            timeout=args.timeout,
            concurrency=args.concurrency,
        )

        host_results = await host_runner.run(
            hosts=hosts,
            ports=ports,
            scan_type=args.scan_type,
        )
        for host_result in host_results:

            if host_result.success:
                ResultFormatter.print(host_result.data)

            else:
                print(
                    f"{host_result.host}\tERROR ({host_result.error})"
                )