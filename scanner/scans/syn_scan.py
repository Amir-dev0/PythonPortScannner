import struct
import random
import socket
from scanner.async_runner import AsyncRunner, TaskContext
from scanner.constants import PortState
from scanner.models.scan_info import ScanInfo
from scanner.core.base_scanner import BaseScanner
from scanner.cli.progress import ProgressReporter

class SynScanner(BaseScanner):

    async def scan(
        self,
        context: TaskContext,
    ):
        return await self._syn_scan(context)

    async def _syn_scan(
        self,
        context: TaskContext
    ):
        """
        Perform a TCP SYN scan on a single port.
        """

        destination_ip = socket.gethostbyname(context.host)

        source_ip = self._get_local_ip(
            destination_ip
        )

        source_port = self._generate_source_port()

        packet = self._build_packet(
            source_ip=source_ip,
            destination_ip=destination_ip,
            source_port=source_port,
            destination_port=context.port
        )

        sock = self._create_socket()

        try:

            self._send_packet(
                sock,
                packet,
                destination_ip
            )

            response = self._receive_packet(
                sock=sock,
                expected_source_ip=destination_ip,
                expected_destination_port=source_port
            )

            if response is None:
                return ScanInfo(
                    state=PortState.FILTERED
                )
            
            return self._parse_response(response)

        finally:

            sock.close()
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

    def _receive_packet(
        self,
        sock,
        expected_source_ip: str,
        expected_destination_port: int
    ):
        """
        Receive packets until the matching TCP response is found.
        """

        while True:

            try:
                packet, _ = sock.recvfrom(65535)

            except socket.timeout:
                return None

            ip = self._parse_ip_header(packet)

            if ip["protocol"] != socket.IPPROTO_TCP:
                continue

            if ip["source_ip"] != expected_source_ip:
                continue

            tcp = self._parse_tcp_header(
                packet,
                ip["header_length"]
            )

            if tcp["destination_port"] != expected_destination_port:
                continue

            return packet
    def _parse_ip_header(self, packet: bytes): 
        ip_header = packet[:20]

        fields = struct.unpack(
            "!BBHHHBBH4s4s",
            ip_header
        )

        version_ihl = fields[0]

        ihl = version_ihl & 0x0F

        header_length = ihl * 4

        source_ip = socket.inet_ntoa(fields[8])

        destination_ip = socket.inet_ntoa(fields[9])

        protocol = fields[6]

        return {
            "header_length": header_length,
            "source_ip": source_ip,
            "destination_ip": destination_ip,
            "protocol": protocol
        }
    def _parse_tcp_header(
        self,
        packet: bytes,
        ip_header_length: int
    ):
        tcp_header = packet[
        ip_header_length:
        ip_header_length + 20
        ]

        fields = struct.unpack(
            "!HHLLBBHHH",
            tcp_header
        )
        source_port = fields[0]

        destination_port = fields[1]

        sequence = fields[2]

        acknowledgement = fields[3]

        offset = fields[4] >> 4

        flags = fields[5]

        return {
        "source_port": source_port,
        "destination_port": destination_port,
        "sequence": sequence,
        "acknowledgement": acknowledgement,
        "flags": flags,
        "header_length": offset * 4
        }
    def _generate_source_port(self) -> int:

        """
        Generate a random ephemeral source port.
        """

        return random.randint(49152, 65535)
    
    def _parse_response(
        self,
        packet: bytes
    ):
        """
        Parse the TCP response packet and determine the port state.
        """

        SYN = 0x02
        ACK = 0x10
        RST = 0x04

        ip = self._parse_ip_header(packet)

        tcp = self._parse_tcp_header(
            packet,
            ip["header_length"]
        )

        flags = tcp["flags"]

        if (flags & (SYN | ACK)) == (SYN | ACK):
            return ScanInfo(
                endpoint="raw-packet",
                state=PortState.OPEN,
            )
        if flags & RST:
            return ScanInfo(
                endpoint="raw-packet",
                state=PortState.CLOSED,
            )

        return ScanInfo(
            endpoint="raw-packet",
            state=PortState.UNKNOWN,
        )