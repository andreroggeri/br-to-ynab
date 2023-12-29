import locale
from datetime import datetime
from typing import Iterable, List

from dateutil.relativedelta import relativedelta
from pynubank import Nubank

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction

locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')


def _is_active_transactions(transaction: dict):
    return transaction['details']['status'] == 'settled'


def _is_installment_transaction(transaction: dict):
    return 'charges' in transaction['details']


class NubankCreditCardData(DataImporter):
    
    def __init__(self, nubank: Nubank, account_id: str):
        self.nu = nubank
        self.account_id = account_id
    
    def get_data(self) -> Iterable[Transaction]:
        transactions = self.nu.get_card_statements()
        active_transactions = list(filter(_is_active_transactions, transactions))
        cash_transactions = filter(lambda x: not _is_installment_transaction(x), active_transactions)
        installment_transactions = filter(_is_installment_transaction, active_transactions)
        
        formatted_cash_transactions = map(self._card_data_to_transaction, cash_transactions)
        formatted_installment_transactions = map(self._expand_installment_transaction, installment_transactions)
        accumulated_installment_transactions = [item for sublist in formatted_installment_transactions for item in
                                                sublist]
        
        return list(formatted_cash_transactions) + accumulated_installment_transactions
    
    def _card_data_to_transaction(self, card_transaction: dict) -> Transaction:
        return {
            'transaction_id': card_transaction['id'],
            'account_id': self.account_id,
            'amount': card_transaction['amount'] * 10 * -1,
            'payee': card_transaction['description'],
            'date': card_transaction['time'][:10],
            'memo': '',
            'flag': None
        }
    
    def _expand_installment_transaction(self, transaction: dict) -> List[Transaction]:
        count = transaction['details']['charges']['count']
        installment_amount = transaction['details']['charges']['amount'] * 10 * -1
        parsed_date = datetime.strptime(transaction['time'][:10], '%Y-%m-%d')
        
        def _to_transaction(index) -> Transaction:
            formatted_value = locale.currency(transaction['amount'] / 100, grouping=True)
            # Adds the index to the date so the transactions spans multiple months
            date = (parsed_date + relativedelta(months=index)).strftime('%Y-%m-%d')
            return {
                'transaction_id': f'{transaction["id"]}-{index}',
                'account_id': self.account_id,
                'payee': transaction['description'],
                'amount': installment_amount,
                'date': date,
                'memo': f'Parcela {index} de {count}. Valor total: {formatted_value}',
                'flag': 'Parcelado'
            }
        
        return [_to_transaction(i + 1) for i in range(count)]
