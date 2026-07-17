from scanner.output.csv_writer import CsvWriter
from scanner.output.json_writer import JsonWriter


class OutputFactory:

    @staticmethod
    def create(format_name: str):

        format_name = format_name.lower()

        if format_name == "json":
            return JsonWriter()

        if format_name == "csv":
            return CsvWriter()

        raise ValueError(
            f"Unsupported output format: {format_name}"
        )