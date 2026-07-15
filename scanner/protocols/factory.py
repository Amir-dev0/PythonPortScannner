from scanner.protocols.http import HTTPProtocol
from scanner.protocols.ssh import SSHProtocol
from scanner.protocols.ftp import FTPProtocol
from scanner.protocols.smtp import SMTPProtocol
from scanner.protocols.generic import GenericProtocol


HTTP_PORTS = {80, 8000, 8080, 8888}
SSH_PORTS = {22, 2222}
FTP_PORTS = {21}
SMTP_PORTS = {25}


class ProtocolFactory:

    @staticmethod
    def create(port: int):

        if port in HTTP_PORTS:
            return HTTPProtocol()

        if port in SSH_PORTS:
            return SSHProtocol()

        if port in FTP_PORTS:
            return FTPProtocol()

        if port in SMTP_PORTS:
            return SMTPProtocol()

        return GenericProtocol()