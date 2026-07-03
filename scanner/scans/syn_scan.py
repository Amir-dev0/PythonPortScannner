import struct
import random
import socket
from scanner.async_runner import AsyncRunner, TaskContext


class SynScanner:

    def __init__(self):

        self.runner = AsyncRunner()

    async def scan(self, host, ports):

        pass

    async def _syn_scan(self, context):

        pass

    def _build_packet(self, source_ip,destination_ip, source_port, destination_port):
        
        sequence = random.randint(0, 0xFFFFFFFF)

        acknowledgement = 0

        data_offset = 5

        reserved = 0

        syn_flag = 0x02

        offset_reserved_flags = (
            data_offset << 12
        ) | (
            reserved << 9
        ) | syn_flag

        window = 64240

        urgent_pointer = 0

        packet = struct.pack(
            "!HHLLHHHH",
            source_port,
            destination_port,
            sequence,
            acknowledgement,
            offset_reserved_flags,
            window,
            0,
            urgent_pointer
        )
        pseudo_header = self._build_pseudo_header(
            source_ip,
           destination_ip,
           len(packet)
        )

        checksum = self._calculate_checksum(pseudo_header + packet)

        packet = struct.pack(
            "!HHLLHHHH",
            source_port,
            destination_port,
            sequence,
            acknowledgement,
            offset_reserved_flags,
            window,
            checksum,
            urgent_pointer
        )
        return packet

    def _parse_response(self):
        pass

    def _calculate_checksum(self, data: bytes):

        """
        Calculate the Internet checksum (RFC 1071).
        """

        if len(data) % 2:
            data += b"\x00"

        checksum = 0

        for i in range(0, len(data), 2):

            word = (data[i] << 8) + data[i + 1]

            checksum += word

            checksum = (
                checksum & 0xFFFF
            ) + (
                checksum >> 16
            )

        checksum = ~checksum & 0xFFFF

        return checksum
    
    def _build_pseudo_header(self, source_ip, destination_ip, tcp_length):

        source_ip = socket.inet_aton(source_ip)

        destination_ip = socket.inet_aton(destination_ip)

        reserved = 0

        protocol = socket.IPPROTO_TCP

        return struct.pack(
            "!4s4sBBH",
            source_ip,
            destination_ip,
            reserved,
            protocol,
            tcp_length
        )

    def _get_local_ip(self, destination_ip):

        """
        Return the local IP address that would be used to reach
        the destination host.
        """

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )

        try:

            sock.connect(
                (destination_ip, 80)
            )

            return sock.getsockname()[0]

        finally:

            sock.close()
    def _create_socket(self):

        """
        Create a raw TCP socket.
        """

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_RAW,
            socket.IPPROTO_TCP
        )

        sock.settimeout(3)

        return sock
    
    def _send_packet(
        self,
        sock,
        packet,
        destination_ip
    ):

        sock.sendto(
            packet,
            (
                destination_ip,
                0
            )
        )

async def main():

    scanner = SynScanner()

    destination_ip = "8.8.8.8"

    local_ip = scanner._get_local_ip(destination_ip)

    packet = scanner._build_packet(
        source_ip=local_ip,
        destination_ip=destination_ip,
        source_port=50000,
        destination_port=80
    )

    print(packet.hex())
    print(len(packet))

    fields = struct.unpack("!HHLLHHHH", packet)

    print(fields)
    sock = scanner._create_socket()

    print(sock)
    sock = scanner._create_socket()

    scanner._send_packet(
        sock,
        packet,
        destination_ip
    )

    print("Packet Sent")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())    