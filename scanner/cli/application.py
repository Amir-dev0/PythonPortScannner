from scanner.async_runner import AsyncRunner
from scanner.cli.parser import CLIParser
from scanner.factory.scanner_factory import ScannerFactory
from scanner.parser.host_parser import HostParser
from scanner.parser.port_parser import PortParser
from scanner.core.task_context import TaskContext
from scanner.cli.formatter import ResultFormatter
from scanner.output.factory import OutputFactory
from scanner.cli.progress import RichProgressReporter


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

        hosts = self._host_parser.parse(args.host)
        ports = self._port_parser.parse(args.ports)

        contexts = [
            TaskContext(
                factory=scanner.scan,
                host=host,
                port=port,
                scan_type=args.scan_type,
            )
            for host in hosts
            for port in ports
        ]

        runner = AsyncRunner(
            timeout=args.timeout,
            limit=args.concurrency,
            reporter=RichProgressReporter(),
        )

        results = await runner.run(contexts)

        if args.output:

            writer = OutputFactory.create(
                args.output.suffix.lstrip(".")
            )

            writer.write(
                results,
                str(args.output),
            )

        ResultFormatter.print(results)