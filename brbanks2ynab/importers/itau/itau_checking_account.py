import hashlib
from datetime import datetime
from typing import Iterable

from pyitau import Itau

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction


class ItauCheckingAccount(DataImporter):
    def __init__(self, itau: Itau, account_id: str):
        self.itau = itau
        self.account_id = account_id

    def get_data(self) -> Iterable[Transaction]:
        statements = self.itau.get_statements()
        transactions = filter(self._is_useful_transaction, statements['lancamentos'])
        return map(self._to_transaction, transactions)

    def _to_transaction(self, itau_transaction: dict) -> Transaction:
        # Parses the date in this format: 11/01/2023
        date = datetime.strptime(itau_transaction['dataLancamento'], '%d/%m/%Y')
        amount = float(itau_transaction['valorLancamento'].replace('.', '').replace(',', '.'))
        is_inflow = itau_transaction['ePositivo']
        description = itau_transaction['descricaoLancamento']
        tx_id = hashlib.sha1(f'{date.isoformat()}:{amount}:{is_inflow}:{description}'.encode('utf-8')).hexdigest()

        if not is_inflow:
            amount *= -1

        return {
            'transaction_id': str(tx_id),
            'account_id': self.account_id,
            'payee': description,
            'amount': int(amount * 1000),
            'date': date.strftime('%Y-%m-%d'),
        }

    def _is_useful_transaction(self, transaction: dict):
        return transaction['dataLancamento'] is not None \
            and 'SALDO DO DIA' not in transaction['descricaoLancamento'] \
            and 'SALDO ANTERIOR' not in transaction['descricaoLancamento']
