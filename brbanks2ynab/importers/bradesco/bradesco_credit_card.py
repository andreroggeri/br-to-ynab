import uuid
from datetime import datetime
from typing import Iterable

from pybradesco import Bradesco, BradescoTransaction

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction


class BradescoCreditCard(DataImporter):

    def __init__(self, bradesco: Bradesco, account_id: str):
        self.bradesco = bradesco
        self.account_id = account_id

    async def get_data(self) -> Iterable[Transaction]:
        transactions = await self.bradesco.get_credit_card_statements()
        transactions = filter(self._past_transactions, transactions)
        transactions = filter(self._ignored_transactions, transactions)
        return map(self._to_transaction, transactions)

    def _to_transaction(self, transaction: BradescoTransaction) -> Transaction:
        transaction_date = transaction.date.strftime('%Y-%m-%d')
        transaction_merged_data = f'{transaction_date}:{transaction.amount}:{transaction.description}'
        transaction_id = str(uuid.uuid5(uuid.NAMESPACE_URL, transaction_merged_data))
        return {
            'transaction_id': transaction_id,
            'account_id': self.account_id,
            'payee': transaction.description,
            'amount': int(transaction.amount * 100) * -1,
            'date': transaction_date,
        }

    def _past_transactions(self, transaction: BradescoTransaction) -> bool:
        return transaction.date <= datetime.now()

    def _ignored_transactions(self, transaction: BradescoTransaction) -> bool:
        ignored_transactions = ['Saldo Anterior', 'bx Autom Fundos', 'Aplicacao em Fundos']
        return not any(t in transaction.description for t in ignored_transactions)
