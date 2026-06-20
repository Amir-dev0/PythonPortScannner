import socket

class PortScanner:

    def __init__(self, target):
        self.target = target

    def scan_port(self, port):
        sock = socket.socket()
        sock.settimeout(2)

        try:
            sock.connect((self.target, port))
            return "open"
        except OSError:
            return "closed"
        finally:
            sock.close()

    def scan_range(self, begin=1, end=65535):
        results = []

        for port in range(begin, end + 1):
            status = self.scan_port(port)
            results.append(f"port {port} is {status}")

        return "\n".join(results)


scanner = PortScanner("localhost")
print(scanner.scan_range())