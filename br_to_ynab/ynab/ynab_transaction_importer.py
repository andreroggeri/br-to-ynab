from datetime import datetime
from typing import List

from ynab_sdk import YNAB
from ynab_sdk.api.models.requests.transaction import TransactionRequest

from br_to_ynab.importers.data_importer import DataImporter
from br_to_ynab.importers.transaction import Transaction


class YNABTransactionImporter:
    def __init__(self, ynab: YNAB, budget_id: str, starting_date: str):
        self.ynab = ynab
        self.budget_id = budget_id
        self.starting_date = datetime.strptime(starting_date, '%Y-%m-%d')
        self.transactions: List[TransactionRequest] = []

    def get_transactions_from(self, transaction_importer: DataImporter):
        transactions = transaction_importer.get_data()
        transactions = filter(self._filter_transaction, transactions)
        transformed = map(self._create_transaction_request, transactions)
        self.transactions.extend(transformed)
        return self

    def save(self):
        return self.ynab.transactions.create_transactions(self.budget_id, self.transactions)

    def _create_transaction_request(self, transaction: Transaction) -> TransactionRequest:
        return TransactionRequest(
            transaction['account_id'],
            transaction['date'],
            transaction['amount'],
            payee_name=transaction['payee'],
            import_id=transaction['transaction_id'],
        )

    def _filter_transaction(self, transaction: Transaction) -> bool:
        transaction_date = datetime.strptime(transaction['date'], '%Y-%m-%d')

        return transaction_date >= self.starting_date
