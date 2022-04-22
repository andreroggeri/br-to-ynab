import uuid
from typing import Iterable

from pybradesco import Bradesco
from pybradesco.bradesco_transaction import BradescoTransaction

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction


class BradescoCheckingAccount(DataImporter):

    def __init__(self, bradesco: Bradesco, account_id: str):
        self.bradesco = bradesco
        self.account_id = account_id

    async def get_data(self) -> Iterable[Transaction]:
        transactions = await self.bradesco.get_checking_account_statements()

        return map(self._to_transaction, transactions)

    def _to_transaction(self, transaction: BradescoTransaction) -> Transaction:
        transaction_date = transaction.date.strftime('%Y-%m-%d')
        transaction_merged_data = f'{transaction_date}:{transaction.amount}:{transaction.description}'
        transaction_id = str(uuid.uuid5(uuid.NAMESPACE_URL, transaction_merged_data))
        return {
            'transaction_id': transaction_id,
            'account_id': self.account_id,
            'payee': transaction.description,
            'amount': int(transaction.amount * 100),
            'date': transaction_date,
        }
