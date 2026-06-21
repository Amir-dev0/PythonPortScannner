import asyncio

class PortScanner():

    def __init__(
            self,
            target,
            timeout = 2.5,
            workers = 300
    ):
        self.open_ports = []
        self.target = target
        self.timeout = timeout
        self.workers = workers
    async def scan(self, port: int):
        
        try:
            reader, writer = await asyncio.wait_for(
                asyncio.open_connection(self.target, port),
                timeout = self.timeout
            )
            self.open_ports.append(port)
            print(f"[+] {port} OPEN")
            writer.close()
            await writer.wait_closed()

        except(
            asyncio.TimeoutError,
            ConnectionRefusedError,
            OSError
        ):
            pass

    async def worker(self, queue: asyncio.Queue):

        try:
            while True:
                port = await queue.get()

                try:
                    await self.scan(port)

                finally:
                    queue.task_done()

        except asyncio.CancelledError:
            return
        
    async def main(self):

        queue = asyncio.Queue()

        for port in range(1,65536):
            await queue.put(port)
        
        workers = [
            asyncio.create_task(self.worker(queue))
            for _ in range(self.workers)
        ]

        await queue.join()

        for w in workers:
            w.cancel()

        await asyncio.gather(
            *workers,
            return_exceptions=True
        )

        for port in sorted(self.open_ports):
            print(f"   {port}")

scanner = PortScanner("127.0.0.1")
asyncio.run(scanner.main())