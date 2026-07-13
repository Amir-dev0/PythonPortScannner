from scanner.async_runner import TaskResult


class ResultFormatter:

    @staticmethod
    def print(results):

        for result in results:

            endpoint = result.host

            if result.port is not None:
                endpoint += f":{result.port}"

            if not result.success:
                print(
                    f"{endpoint}\tERROR ({result.error})"
                )
                continue

            message = (
                f"{endpoint}\t"
                f"{result.data.state.value}"
            )

            if result.data.banner:
                message += f" | {result.data.banner}"

            if result.data.service:
                message += f" | Service: {result.data.service}"

            if result.data.version:
                message += f" | Version: {result.data.version}"

            print(message)