class PortParser:

    def parse(self, ports: str) -> list[int]:

        result = []

        for item in ports.split(","):

            item = item.strip()

            if "-" in item:

                start, end = item.split("-")

                start = int(start)
                end = int(end)

                if start > end:
                    raise ValueError(
                        f"Invalid port range: {start}-{end}"
                    )

                result.extend(
                    range(start, end + 1)
                )

            else:

                result.append(int(item))

        return self._validate(result)

    def _validate(self, ports: list[int]) -> list[int]:

        validated = []

        for port in ports:

            if port < 1 or port > 65535:
                raise ValueError(
                    f"Invalid port: {port}"
                )

            validated.append(port)

        return sorted(set(validated))    