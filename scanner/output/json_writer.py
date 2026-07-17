import json
from dataclasses import asdict
from scanner.models.scan_info import ScanInfo
from scanner.output.base import OutputWriter


class JsonWriter(OutputWriter):

    def write(
        self,
        results: list[ScanInfo],
        output: str,
    ) -> None:

        data = [
            asdict(result)
            for result in results
        ]

        with open(
            output,
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
            )