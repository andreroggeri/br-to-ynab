import unittest
from typing import List
from unittest.mock import patch

from pynubank import Nubank, MockHttpClient

from brbanks2ynab.importers.nubank.nubank_checking_account import NubankCheckingAccountData


def find_transaction_idx_by_type(transactions, expected_type):
    return next((i for i, item in enumerate(transactions) if item['__typename'] == expected_type))


class TestNubankCheckingAccount(unittest.TestCase):
    nu: Nubank
    nu_transactions: List[dict]

    def setUp(self) -> None:
        self.nu = Nubank(client=MockHttpClient())
        self.nu.authenticate_with_qr_code('1234', '1234', 'uuid')
        self.nu_transactions = self.nu.get_account_statements()

    def test_should_import_barcode_transactions_using_detail_as_payee(self):
        nu_checking_account = NubankCheckingAccountData(self.nu, 'some-id')

        idx = find_transaction_idx_by_type(self.nu_transactions, 'BarcodePaymentEvent')

        imported_transactions = list(nu_checking_account.get_data())

        self.assertEqual(imported_transactions[idx]['payee'], self.nu_transactions[idx]['detail'])

    def test_should_import_transferout_transactions_using_destination_account_as_payee(self):
        nu_checking_account = NubankCheckingAccountData(self.nu, 'some-id')

        idx = find_transaction_idx_by_type(self.nu_transactions, 'TransferOutEvent')

        imported_transactions = list(nu_checking_account.get_data())

        self.assertEqual(imported_transactions[idx]['payee'], self.nu_transactions[idx]['destinationAccount']['name'])

    def test_should_import_transferin_transactions_using_origin_account_as_payee(self):
        nu_checking_account = NubankCheckingAccountData(self.nu, 'some-id')

        idx = find_transaction_idx_by_type(self.nu_transactions, 'TransferInEvent')

        imported_transactions = list(nu_checking_account.get_data())

        self.assertEqual(imported_transactions[idx]['payee'], self.nu_transactions[idx]['originAccount']['name'])

    def test_should_import_bill_payent_transactions_using_title_as_payee(self):
        nu_checking_account = NubankCheckingAccountData(self.nu, 'some-id')

        idx = find_transaction_idx_by_type(self.nu_transactions, 'BillPaymentEvent')

        imported_transactions = list(nu_checking_account.get_data())

        self.assertEqual(imported_transactions[idx]['payee'], self.nu_transactions[idx]['title'])

    def test_should_import_unmapped_transactions_using_title_and_detail_as_payee(self):
        nu_checking_account = NubankCheckingAccountData(self.nu, 'some-id')

        changed_transaction = self.nu_transactions[0]
        changed_transaction['__typename'] = 'UnmappedEvent'
        with patch.object(self.nu, 'get_account_statements', return_value=[changed_transaction]):
            imported_transactions = list(nu_checking_account.get_data())

        self.assertEqual(imported_transactions[0]['payee'],
                         f'{self.nu_transactions[0]["title"]} {self.nu_transactions[0]["detail"]}')
