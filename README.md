# PythonPortScanner

A modern asynchronous TCP port scanner written in Python, built with a modular architecture and designed for extensibility.

Rather than being just another port scanner, this project focuses on clean code, object-oriented design, asynchronous execution, and building a solid foundation for more advanced network scanning features.

---

## Features

### Implemented

* Asynchronous scanning using `asyncio`
* Configurable concurrency with `AsyncRunner`
* Retry mechanism
* Timeout handling
* TCP Connect Scan
* SYN Scan (Raw Socket)
* Banner Grabbing
* Command Line Interface (CLI)
* Scanner Factory pattern
* Structured scan results using `TaskResult`
* Unit tests with `pytest`

---

## Project Structure

```text
scanner/
│
├── async_runner.py
│
├── cli/
│   ├── application.py
│   └── parser.py
│
├── factory/
│   └── scanner_factory.py
│
├── parser/
│   └── port_parser.py
│
├── scans/
│   ├── connect_scan.py
│   ├── banner_scan.py
│   └── syn_scan.py
│
├── services/
│   └── banner.py
│
├── fingerprint/
│   └── os_detection.py
│
└── __init__.py
```

---

## Current Scanners

| Scanner         | Status         |
| --------------- | -------------- |
| Connect Scan    | ✅ Implemented  |
| Banner Grabbing | ✅ Implemented  |
| SYN Scan        | ✅ Implemented  |
| OS Detection    | 🚧 In Progress |

---

## Planned Features

* UDP Scan
* Service Version Detection
* OS Fingerprinting Improvements
* Port Range Parsing (`1-1024`)
* JSON Export
* CSV Export
* Better CLI Output
* IPv6 Support

---

## Running Tests

Run all tests:

```bash
pytest
```

Run a specific test module:

```bash
pytest tests/test_syn_scan.py
```

---

## Examples

Run a Connect Scan:

```bash
python main.py scanme.nmap.org
```

Scan multiple ports:

```bash
python main.py scanme.nmap.org -p 22,80,443
```

Choose a scan type:

```bash
python main.py scanme.nmap.org --scan-type connect
```

---

## Design Goals

This project is built around the following principles:

* Clean Architecture
* Object-Oriented Design
* Asynchronous Programming
* Extensibility
* Maintainability
* Testability

The long-term goal is to evolve PythonPortScanner into a modular, production-quality network scanning tool while keeping the codebase clean and easy to extend.
