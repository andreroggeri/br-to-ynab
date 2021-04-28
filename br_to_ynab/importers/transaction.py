from typing import TypedDict


class Transaction(TypedDict):
    transaction_id: str
    account_id: str
    payee: str
    amount: int
    date: str
