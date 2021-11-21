from datetime import datetime, timedelta
from typing import Iterable, List

from ynab_sdk.api.models.responses.accounts import Account

from brbanks2ynab.importers import DataImporter, Transaction
from pynuinvest import NuInvest


class NuInvestImporter(DataImporter):

    def __init__(self, account: Account, nu: NuInvest):
        self.account = account
        self.nu = nu

    def get_data(self) -> Iterable[Transaction]:
        statements = self._get_account_statements()
        statements.append(self._get_account_profits(statements))
        return statements

    def _to_transaction(self, data: dict) -> Transaction:
        return {
            'transaction_id': data['statementNumber'],
            'account_id': self.account.id,
            'payee': data['description'],
            'amount': data['value'] * 100,
            'date': data['movementDate'][:10],
        }

    def _filter_transactions(self, data: dict):
        inflow_codes = [26, 118, 200, 22]
        return data['historyCode'] in inflow_codes

    def _get_account_statements(self):
        start_date = datetime.now() - timedelta(days=30)
        end_date = datetime.now()
        response = self.nu.get_account_statements(start_date, end_date)
        transactions = filter(self._filter_transactions, response['statements'])
        return list(map(self._to_transaction, transactions))

    def _get_account_profits(self, transactions: List[Transaction]):
        investment_data = self.nu.get_investment_data()
        transactions_sum = sum(map(lambda x: x['amount'], transactions))
        current_balance = investment_data['totalBalance']
        new_balance = self.account.balance + transactions_sum

        profit_transaction: Transaction = {
            'transaction_id': '',
            'account_id': self.account.id,
            'payee': 'NuInvest',
            'amount': new_balance - current_balance,
            'date': datetime.now().strftime('%Y-%m-%d')
        }

        return profit_transaction
