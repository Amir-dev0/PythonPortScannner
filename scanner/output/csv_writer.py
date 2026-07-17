import csv
from dataclasses import asdict
from scanner.models.scan_info import ScanInfo
from scanner.output.base import OutputWriter


class CsvWriter(OutputWriter):

    def write(
        self,
        results: list[ScanInfo],
        output: str,
    ) -> None:

        if not results:
            return

        with open(
            output,
            "w",
            newline="",
            encoding="utf-8",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=asdict(results[0]).keys(),
            )

            writer.writeheader()

            for result in results:
                writer.writerow(
                    asdict(result)
                )