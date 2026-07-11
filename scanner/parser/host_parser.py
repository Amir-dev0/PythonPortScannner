import ipaddress


class HostParser:
    """
    Parse target hosts.

    Supported formats:

    - Hostname
    - IPv4 address
    - IPv4 CIDR
    """

    def parse(
        self,
        target: str,
    ) -> list[str]:

        target = target.strip()

        if "/" in target:
            return self._parse_cidr(target)

        return [target]

    def _parse_cidr(
        self,
        target: str,
    ) -> list[str]:

        network = ipaddress.ip_network(
            target,
            strict=False,
        )

        return [
            str(host)
            for host in network.hosts()
        ]