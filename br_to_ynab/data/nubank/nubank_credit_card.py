from typing import Iterable

from pynubank import Nubank

from br_to_ynab.data.data_importer import DataImporter
from br_to_ynab.data.transaction import Transaction


class NubankCreditCardData(DataImporter):

    def __init__(self, nubank: Nubank, account_id: str):
        self.nu = nubank
        self.account_id = account_id

    def get_data(self) -> Iterable[Transaction]:
        transactions = self.nu.get_card_statements()

        return map(self._card_data_to_transaction, transactions)

    def _card_data_to_transaction(self, card_transaction: dict) -> Transaction:
        return {
            'transaction_id': card_transaction['id'],
            'account_id': self.account_id,
            'amount': card_transaction['amount'] * 10 * -1,
            'payee': card_transaction['description'],
            'date': card_transaction['time'][:10],
        }
