# PythonPortScanner

A modular and asynchronous port scanner written in Python, designed with extensibility, maintainability, and performance in mind.

Unlike simple socket-based scanners, this project provides a clean architecture that makes it easy to add new scan techniques, integrate additional services, and scale the project over time.

---

## Features

* TCP Connect Scan
* SYN Scan
* Banner Grabbing
* Asynchronous scanning with `asyncio`
* Configurable concurrency limits
* Automatic retry mechanism
* Timeout handling
* Scanner Factory Pattern
* Modular architecture
* CLI interface
* Unit tests with `pytest`

---

## Project Structure

```text
PythonPortScanner/
│
├── scanner/
│   ├── cli/
│   ├── core/
│   ├── factory/
│   ├── fingerprint/
│   ├── parser/
│   ├── scans/
│   └── services/
│
├── tests/
├── requirements.txt
└── main.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/Amir-dev0/PythonPortScannner.git
cd PythonPortScannner
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate it:

Linux/macOS

```bash
source venv/bin/activate
```

Windows

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

Example:

```bash
python main.py --target scanme.nmap.org --ports 1-1000
```

or

```bash
python main.py --target 192.168.1.10 --ports 22,80,443
```

Run banner grabbing:

```bash
python main.py --target scanme.nmap.org --banner
```

---

## Architecture

The project follows a modular architecture.

* **core** – Shared infrastructure and async execution.
* **factory** – Creates scanner implementations.
* **scans** – Contains scan techniques.
* **services** – Shared services used by scanners.
* **parser** – Parses user input.
* **cli** – Command-line interface.
* **fingerprint** – Network fingerprinting components.

This separation allows new scan methods to be added with minimal changes to the existing codebase.

---

## Testing

Run all tests:

```bash
pytest
```

or

```bash
pytest -v
```

---

## Technologies

* Python 3
* asyncio
* socket
* argparse
* pytest

---

## Roadmap

* [ ] UDP Scan
* [ ] Service Detection
* [ ] Version Detection
* [ ] CIDR Network Scan
* [ ] JSON/XML Export
* [ ] Progress Bar
* [ ] Logging System
* [ ] IPv6 Support

---

## Why This Project?

This project is built as a learning and portfolio project with a focus on:

* Clean Architecture
* Asynchronous Programming
* Network Programming
* Software Design Principles
* Testable Code
* Extensible Scanner Framework

The goal is not only to perform port scanning but also to build a maintainable networking tool that can be extended with additional scanning techniques and network analysis features.

---

## License

This project is licensed under the MIT License.
