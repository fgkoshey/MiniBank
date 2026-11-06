# MiniBank

MiniBank is a lightweight banking simulator written in Python. It supports money transfers between accounts and keeps a history of successful transactions.

## Features

- **Money Transfers:** Send money between existing accounts.
- **Transaction Validation:** Check account existence, available balance, and transfer amounts.
- **Transaction History:** Record successful transfers.
- **Automated Tests:** Test transfer functionality using pytest.

## Installation

Clone the repository:

```bash
git clone https://github.com/fgkoshey/MiniBank.git
```

Navigate to the project directory:

```bash
cd MiniBank
```

## Running the Application

```bash
py bank.py
```

## Running Tests

Install pytest:

```bash
py -m pip install pytest
```

Run the tests:

```bash
py -m pytest -v
```

## Project Status

This project is under active development. Future improvements will include persistent storage, a database, and a REST API.