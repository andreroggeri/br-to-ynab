from pynubank import Nubank

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction
from brbanks2ynab.util import deep_get

OUTFLOW_EVENT_TYPES = (
    'TransferOutEvent',
    'TransferOutReversalEvent',
    'BarcodePaymentEvent',
    'DebitPurchaseEvent',
    'DebitPurchaseReversalEvent',
    'BillPaymentEvent',
    'DebitWithdrawalFeeEvent',
    'DebitWithdrawalEvent',
    'PixTransferOutEvent',
)


class NubankCheckingAccountData(DataImporter):
    
    def __init__(self, nubank: Nubank, account_id: str):
        self.nu = nubank
        self.account_id = account_id
    
    def get_data(self):
        transactions = self.nu.get_account_statements()
        
        return map(self._account_data_to_transaction, transactions)
    
    def _account_data_to_transaction(self, account_transaction: dict) -> Transaction:
        return {
            'transaction_id': account_transaction['id'],
            'account_id': self.account_id,
            'amount': self._get_transaction_amount(account_transaction),
            'payee': self._get_payee_from_acct_transaction(account_transaction),
            'date': account_transaction['postDate'],
            'memo': '',
            'flag': None
        }
    
    def _get_transaction_amount(self, account_transaction: dict) -> int:
        amount = int(account_transaction['amount'] * 1000)
        if account_transaction['__typename'] in OUTFLOW_EVENT_TYPES:
            amount *= -1
        return amount
    
    def _get_payee_from_acct_transaction(self, account_transaction: dict) -> str:
        transaction_type_map = {
            'BarcodePaymentEvent': 'detail',
            'TransferOutEvent': 'destinationAccount.name',
            'TransferInEvent': 'originAccount.name',
            'BillPaymentEvent': 'title',
        }
        
        field = transaction_type_map.get(account_transaction['__typename'])
        if field:
            return deep_get(account_transaction, field)
        
        return f'{account_transaction["title"]} {account_transaction["detail"]}'
