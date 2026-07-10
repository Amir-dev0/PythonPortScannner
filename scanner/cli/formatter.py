from scanner.async_runner import TaskResult


class ResultFormatter:

    @staticmethod
    def print(results: list[TaskResult]) -> None:

        for result in results:

            if result.success:

                print(
                    f"{result.host}:{result.port:<5} {result.data.value}"
                )

            else:

                print(
                    f"{result.host}:{result.port:<5} ERROR ({result.error})"
                )