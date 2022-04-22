import logging
from datetime import datetime
from typing import List

from actualbudget.actualbudget import ActualBudget
from actualbudget.models.transaction import ABTransaction
from ynab_sdk.api.models.requests.transaction import TransactionRequest

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction

logger = logging.getLogger('brbanks2ynab')


class YNABTransactionImporter:
    def __init__(self, actual: ActualBudget, starting_date: str):
        self.actual = actual
        self.starting_date = datetime.strptime(starting_date, '%Y-%m-%d')
        self.transactions: List[TransactionRequest] = []

    async def get_transactions_from(self, transaction_importer: DataImporter):
        transactions = await transaction_importer.get_data()
        transactions = filter(self._filter_transaction, transactions)
        transformed = list(map(self._create_transaction_request, transactions))
        logger.info(f'{len(transformed)} transactions imported for {self.__name__}')
        self.transactions.extend(transformed)
        return self

    async def save(self):
        grouped_transactions = {}
        for t in self.transactions:
            if not grouped_transactions.get(t.account_id):
                grouped_transactions[t.account_id] = []
            grouped_transactions[t.account_id].append(
                ABTransaction(
                    date=t.date,
                    amount=t.amount,
                    payee_name=t.payee_name,
                    imported_id=t.import_id
                )
            )

        for account_id, transaction in grouped_transactions.items():
            await self.actual.import_transactions(account_id, transaction)

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
