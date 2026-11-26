import pytest
from fastapi.testclient import TestClient

import main
from bank import transfer


@pytest.mark.parametrize(
    ("sender", "receiver", "amount"),
    [
        ("missing", "max", 500),
        ("alex", "missing", 500),
        ("alex", "alex", 500),
        ("alex", "max", -500),
        ("alex", "max", 0),
        ("alex", "max", True),
        ("alex", "max", float("nan")),
        ("alex", "max", float("inf")),
    ],
)
def test_invalid_transfer_leaves_state_unchanged(sender, receiver, amount):
    accounts = {"alex": 1500, "max": 1000}
    history = []

    assert transfer(accounts, history, sender, receiver, amount) is False
    assert accounts == {"alex": 1500, "max": 1000}
    assert history == []


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(main, "accounts", {"alex": 1500, "max": 1000})
    monkeypatch.setattr(main, "history", [])
    with TestClient(main.app) as client:
        yield client


def test_get_accounts(client):
    response = client.get("/accounts")

    assert response.status_code == 200
    assert response.json() == [
        {"username": "alex", "balance": 1500},
        {"username": "max", "balance": 1000},
    ]


def test_get_account(client):
    response = client.get("/accounts/alex")

    assert response.status_code == 200
    assert response.json() == {"username": "alex", "balance": 1500}


def test_get_missing_account(client):
    assert client.get("/accounts/missing").status_code == 404


def test_create_transfer_updates_balances_and_history(client):
    assert client.get("/transactions").json() == []
    response = client.post(
        "/transfers", json={"sender": "alex", "receiver": "max", "amount": 500}
    )

    transaction = {"from": "alex", "to": "max", "amount": 500}
    assert response.status_code == 201
    assert response.json() == transaction
    assert client.get("/accounts/alex").json()["balance"] == 1000
    assert client.get("/accounts/max").json()["balance"] == 1500
    history_response = client.get("/transactions")
    assert history_response.status_code == 200
    assert history_response.json() == [transaction]


@pytest.mark.parametrize(
    ("receiver", "amount", "status_code"),
    [
        ("max", 2000, 400),
        ("alex", 500, 400),
        ("max", -100, 400),
        ("missing", 500, 404),
        ("max", "500", 422),
        ("max", True, 422),
    ],
)
def test_rejected_http_transfer_leaves_state_unchanged(client, receiver, amount, status_code):
    response = client.post(
        "/transfers", json={"sender": "alex", "receiver": receiver, "amount": amount}
    )

    assert response.status_code == status_code
    assert client.get("/accounts/alex").json()["balance"] == 1500
    assert client.get("/accounts/max").json()["balance"] == 1000
    assert client.get("/transactions").json() == []


def test_transfer_requires_amount(client):
    response = client.post("/transfers", json={"sender": "alex", "receiver": "max"})

    assert response.status_code == 422
def test_add_account(client):
    response = client.post("/accounts",json={"username": "ivan"})
    assert response.status_code == 201
    assert response.json() == {"username": "ivan","balance": 0}
def test_duplicate(client):
    response = client.post("/accounts",json={"username": "alex"})
    assert response.status_code == 409
    assert client.get("/accounts/alex").json()["balance"] == 1500
@pytest.mark.parametrize(
"payload",
[    {"username": ""},
{"username": "   "},
{}],
)
def test_unvalid_names(client,payload):
    response = client.post("/accounts",json=payload)
    accounts_response = client.get("/accounts")
    assert response.status_code==422
    assert accounts_response.json() == [
    {"username": "alex", "balance": 1500},
    {"username": "max", "balance": 1000}
]
