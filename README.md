# PythonPortScanner

A modern asynchronous TCP port scanner written in Python, designed with a modular architecture and built for extensibility.

The project focuses on clean architecture, concurrency, and maintainability rather than being just another simple port scanner.

---

## Features

- Asynchronous scanning using `asyncio`
- Configurable concurrency limit
- Automatic retry mechanism
- Timeout handling
- TCP Connect Scan
- Banner Grabbing
- Rich task metadata
- Modular scanner architecture
- Comprehensive test suite

---

## Project Structure

```text
scanner/
│
├── async_runner.py        # Asynchronous execution engine
│
├── scans/
│   ├── connect_scan.py
│   ├── banner_scan.py
│   └── syn_scan.py
│
├── fingerprint/
│   └── os_detection.py
│
└── __init__.py
```

---

## Current Scanners

| Scanner | Status |
|---------|--------|
| Connect Scan | ✅ Implemented |
| Banner Grabbing | ✅ Implemented |
| SYN Scan | 🚧 Planned |

---

## Planned Features

- SYN Scan
- UDP Scan
- Service Detection
- Version Detection
- OS Fingerprinting
- JSON Export
- CSV Export
- CLI Interface

---

## Running Tests

Run all tests:

```bash
pytest
```

Run a specific test:

```bash
pytest tests/test_banner_scan.py
```

---

## Example

```python
from scanner.scans.connect_scan import ConnectScanner

scanner = ConnectScanner()

results = await scanner.scan(
    host="scanme.nmap.org",
    ports=[22, 80, 443]
)

for result in results:
    print(result)
```

Banner Scanner:

```python
from scanner.scans.banner_scan import BannerScanner

scanner = BannerScanner()

results = await scanner.scan(
    host="scanme.nmap.org",
    ports=22
)

for result in results:
    print(result)
```

---

## Design Goals

This project is built with the following goals in mind:

- Clean Architecture
- High Performance
- Modularity
- Extensibility
- Testability
- Readability

---

## Usage

```bash
python3 main.py
```
