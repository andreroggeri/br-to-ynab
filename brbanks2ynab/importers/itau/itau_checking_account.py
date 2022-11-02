from typing import Iterable

from pyitau import Itau

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction


class ItauCheckingAccount(DataImporter):
    def __init__(self, itau: Itau, account_id: str):
        self.itau = itau
        self.account_id = account_id

    def get_data(self) -> Iterable[Transaction]:
        transactions = self.itau.get_account_statements()
        return map(self._to_transaction, transactions)

    def _to_transaction(self, itau_transaction: dict) -> Transaction:
        tx_id = hash(f'{itau_transaction["date"]}:{itau_transaction["amount"]}:{itau_transaction["description"]}')
        payee = itau_transaction['details']['name'] if itau_transaction['details'].get('name') else itau_transaction[
            'description']
        return {
            'transaction_id': str(tx_id),
            'account_id': self.account_id,
            'payee': payee,
            'amount': int(itau_transaction['amount'] * 1000),
            'date': itau_transaction['date'].strftime('%Y-%m-%d'),
        }
