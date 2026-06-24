from __future__ import annotations
import argparse
import platform
import re
import subprocess
import sys
from dataclasses import dataclass
from statistics import mean


_KNOWN_DEFAULTS: dict[int, str] = {
    255: "Cisco IOS / Solaris / AIX",
    128: "Windows (modern: 7/8/10/11/Server)",
    64: "Linux / macOS / BSD / Android / modern Unix-like",
    60: "AIX (older)",
    32: "Windows 95/98/ME (legacy)",
}

_SORTED_DEFAULTS = sorted(_KNOWN_DEFAULTS)
_MAX_PLAUSIBLE_HOPS = 30  


@dataclass
class PingResult:
    host: str
    reachable: bool
    ttl_samples: list[int]
    rtt_samples_ms: list[float]
    error: str | None = None

    @property
    def ttl(self) -> int | None:
        return round(mean(self.ttl_samples)) if self.ttl_samples else None

    @property
    def avg_rtt_ms(self) -> float | None:
        return round(mean(self.rtt_samples_ms), 2) if self.rtt_samples_ms else None


@dataclass
class OsGuess:
    label: str
    estimated_hops: int | None
    confidence: str  


def _build_ping_command(host: str, count: int, timeout_sec: int) -> list[str]:
    is_windows = platform.system().lower() == "windows"
    if is_windows:

        return ["ping", "-n", str(count), "-w", str(timeout_sec * 1000), host]

    return ["ping", "-c", str(count), "-W", str(timeout_sec), host]


def ping_host(host: str, count: int = 3, timeout_sec: int = 2) -> PingResult:

    cmd = _build_ping_command(host, count, timeout_sec)

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout_sec * count + 5,  # hard ceiling so we never hang
        )
    except subprocess.TimeoutExpired:
        return PingResult(host, reachable=False, ttl_samples=[], rtt_samples_ms=[],
                           error="Ping process timed out")
    except FileNotFoundError:
        return PingResult(host, reachable=False, ttl_samples=[], rtt_samples_ms=[],
                           error="'ping' executable not found on this system")
    except Exception as exc:  # noqa: BLE001 - last-resort guard, we report it
        return PingResult(host, reachable=False, ttl_samples=[], rtt_samples_ms=[],
                           error=f"Unexpected error running ping: {exc}")

    output = proc.stdout.lower()

    ttl_matches = re.findall(r"ttl[=:\s]+(\d+)", output)
    rtt_matches = re.findall(r"time[=<]([\d.]+)\s*ms", output)

    ttl_samples = [int(v) for v in ttl_matches]
    rtt_samples = [float(v) for v in rtt_matches]

    if not ttl_samples:
        reason = "Host unreachable, blocked by firewall, or invalid address"
        if proc.returncode != 0 and proc.stderr.strip():
            reason = proc.stderr.strip().splitlines()[0]
        return PingResult(host, reachable=False, ttl_samples=[], rtt_samples_ms=[],
                           error=reason)

    return PingResult(host, reachable=True, ttl_samples=ttl_samples, rtt_samples_ms=rtt_samples)


def guess_os(ttl: int) -> OsGuess:

    candidate_default = next((d for d in _SORTED_DEFAULTS if d >= ttl), None)

    if candidate_default is None:
        return OsGuess(label="Unknown (TTL exceeds all known OS defaults)",
                        estimated_hops=None, confidence="low")

    hops = candidate_default - ttl
    label = _KNOWN_DEFAULTS[candidate_default]

    if hops == 0:
        confidence = "high"
    elif hops <= 10:
        confidence = "medium"
    elif hops <= _MAX_PLAUSIBLE_HOPS:
        confidence = "low"
    else:
        return OsGuess(label="Unknown (TTL too low to match any default plausibly)",
                        estimated_hops=hops, confidence="low")

    return OsGuess(label=label, estimated_hops=hops, confidence=confidence)


def _print_report(result: PingResult, guess: OsGuess | None) -> None:
    print(f"\nTarget: {result.host}")
    if not result.reachable:
        print(f"Status: unreachable")
        print(f"Reason: {result.error}")
        return

    print(f"Status: reachable ({len(result.ttl_samples)} replies)")
    print(f"TTL samples: {result.ttl_samples}  -> averaged: {result.ttl}")
    if result.avg_rtt_ms is not None:
        print(f"Average RTT: {result.avg_rtt_ms} ms")

    assert guess is not None
    print(f"OS guess: {guess.label}")
    if guess.estimated_hops is not None:
        print(f"Estimated network hops: {guess.estimated_hops}")
    print(f"Confidence: {guess.confidence}")
    print(
        "\nNote: TTL fingerprinting is heuristic. Custom OS configs, "
        "NAT, load balancers, and firewalls can all shift the observed TTL."
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Passive OS fingerprinting via ICMP TTL analysis."
    )
    parser.add_argument("host", nargs="?", help="Target IP address or hostname")
    parser.add_argument("--count", type=int, default=3, help="Number of pings to send (default: 3)")
    parser.add_argument("--timeout", type=int, default=2, help="Per-ping timeout in seconds (default: 2)")
    args = parser.parse_args()

    host = args.host or input("Enter target IP or hostname: ").strip()
    if not host:
        print("No target provided. Exiting.")
        return 1

    if args.count < 1:
        print("--count must be at least 1")
        return 1

    result = ping_host(host, count=args.count, timeout_sec=args.timeout)
    guess = guess_os(result.ttl) if result.reachable and result.ttl is not None else None

    _print_report(result, guess)
    return 0 if result.reachable else 1


if __name__ == "__main__":
    sys.exit(main())