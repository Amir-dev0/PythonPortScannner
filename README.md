# PythonPortScanner

Modern asynchronous port scanner written in Python with a clean, extensible architecture focused on concurrency, automation, and maintainability.

## Features

* TCP Connect Scan
* SYN Scan
* Banner Grabbing
* Basic Service & Version Detection
* CIDR host expansion (`192.168.1.0/24`)
* Global asyncio task pipeline
* Rich progress bar
* JSON / CSV export
* Retry and timeout handling
* Unit tests with `pytest`

## Architecture

```text
CLI
 └── AsyncRunner
      └── Scanner.scan(context)
```

Each scan task represents a single endpoint (`host:port`), which keeps the execution pipeline simple and highly concurrent.

## Installation

```bash
git clone https://github.com/Amir-dev0/PythonPortScannner.git
cd PythonPortScannner
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

### Connect scan

```bash
python main.py scanme.nmap.org -p 22,80
```

### Banner scan

```bash
python main.py scanme.nmap.org -s banner -p 22
```

### CIDR scan

```bash
python main.py 192.168.1.0/24 -p 22 --timeout 1
```

### Export results

```bash
python main.py scanme.nmap.org -p 22,80 -o results.json
```

## Example Output

```text
Scanning ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 100%
scanme.nmap.org:22    Open
scanme.nmap.org:80    Open
```

## Testing

```bash
pytest -v
```

## Project Status

This project is considered **feature-complete for its educational and DevOps automation scope**.

The stable release includes:

* asynchronous execution pipeline
* concurrent endpoint scanning
* banner grabbing
* service detection
* progress reporting
* structured export

An experimental OS fingerprinting module exists in `scanner/fingerprint/os_detection.py` but is intentionally **not part of the stable CLI release**.

## Technologies

* Python 3.14+
* asyncio
* Rich
* Scapy
* Pytest

## License

MIT
