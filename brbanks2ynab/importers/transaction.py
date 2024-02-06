from typing import TypedDict, Optional


class Transaction(TypedDict):
    transaction_id: str
    account_id: str
    payee: str
    amount: int
    date: str
    memo: Optional[str]
    flag: Optional[str]
