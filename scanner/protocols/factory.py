from scanner.protocols.http import HTTPProtocol
from scanner.protocols.ssh import SSHProtocol
from scanner.protocols.ftp import FTPProtocol
from scanner.protocols.smtp import SMTPProtocol


class ProtocolFactory:

    @staticmethod
    def create(port: int):

        if port == 80:
            return HTTPProtocol()

        if port == 22:
            return SSHProtocol()

        if port == 21:
            return FTPProtocol()

        if port == 25:
            return SMTPProtocol()

        return SSHProtocol()