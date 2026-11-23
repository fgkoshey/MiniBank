from threading import Lock

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, StrictFloat, StrictInt

from bank import accounts, history, transfer

app = FastAPI(title="MiniBank")
bank_lock = Lock()


class TransferRequest(BaseModel):
    sender: str
    receiver: str
    amount: StrictInt | StrictFloat


@app.get("/accounts")
def list_accounts() -> list[dict]:
    with bank_lock:
        return [
            {"username": username, "balance": balance}
            for username, balance in accounts.items()
        ]


@app.get("/accounts/{username}")
def get_account(username: str) -> dict:
    with bank_lock:
        if username not in accounts:
            raise HTTPException(status_code=404, detail="Account not found")
        return {"username": username, "balance": accounts[username]}


@app.post("/transfers", status_code=201)
def create_transfer(request: TransferRequest) -> dict:
    with bank_lock:
        for username in (request.sender, request.receiver):
            if username not in accounts:
                raise HTTPException(status_code=404, detail=f"Account not found: {username}")

        if not transfer(accounts, history, request.sender, request.receiver, request.amount):
            raise HTTPException(
                status_code=400,
                detail="Check the transfer amount, recipient and balance",
            )

        return history[-1].copy()


@app.get("/transactions")
def list_transactions() -> list[dict]:
    with bank_lock:
        return [transaction.copy() for transaction in history]
