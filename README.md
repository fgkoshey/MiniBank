# MiniBank

MiniBank is a small REST API for viewing accounts, transferring money and
reading the history of successful transfers. The banking logic lives in
`bank.py`, and the HTTP routes live in `main.py`.

The app starts with two accounts: `alex` has 1500 and `max` has 1000. Balances
and transaction history live in memory and reset when the process restarts.
Run one worker so that all requests share the same state. The app uses Python
numbers for this exercise. Fractional amounts can have floating-point rounding.

## Tools

Python 3.10+, FastAPI, Pydantic and Uvicorn. Tests use pytest and FastAPI's
TestClient, which uses HTTPX2.

## Set up and run

```bash
git clone https://github.com/fgkoshey/MiniBank.git
cd MiniBank
python -m venv .venv
```

Activate the environment in PowerShell with `.\.venv\Scripts\Activate.ps1`
or on macOS and Linux with `source .venv/bin/activate`. Then run:

```bash
python -m pip install -r requirements.txt
python -m uvicorn main:app --reload
```

Open [Swagger UI](http://127.0.0.1:8000/docs) to try the endpoints.

## API examples

| Method and path | Result |
| --- | --- |
| `GET /accounts` | List usernames and balances |
| `GET /accounts/{username}` | Get a single account |
| `POST /transfers` | Move money and return the new history entry with HTTP 201 |
| `GET /transactions` | List successful transfers in order |

In PowerShell, list the accounts and transfer 500 from Alex to Max:

```powershell
$base = 'http://127.0.0.1:8000'
Invoke-RestMethod "$base/accounts"
Invoke-RestMethod "$base/accounts/alex"
$body = @{ sender = 'alex'; receiver = 'max'; amount = 500 } | ConvertTo-Json
Invoke-RestMethod "$base/transfers" -Method Post -ContentType 'application/json' -Body $body
Invoke-RestMethod "$base/transactions"
```

The new transaction is `{"from":"alex","to":"max","amount":500}`.

- **400**: The transfer is invalid, for example because the sender and
  receiver match, the amount is zero or negative, or the balance is too low.
- **404**: The requested account, sender or receiver does not exist.
- **422**: The request body does not match the Pydantic schema, for example
  because `amount` is missing or is a string.

## Run tests

```bash
python -m pytest -v
```

Unit tests call 	ransfer() with fresh accounts and history. API tests use
TestClient(app) to check status codes and JSON without starting Uvicorn.
