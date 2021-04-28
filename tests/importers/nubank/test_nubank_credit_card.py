import unittest
from typing import List

from pynubank import Nubank, MockHttpClient

from br_to_ynab.importers.nubank.nubank_credit_card import NubankCreditCardData


class TestNubankCheckingAccount(unittest.TestCase):
    nu: Nubank
    nu_transactions: List[dict]

    def setUp(self) -> None:
        self.nu = Nubank(client=MockHttpClient())
        self.nu.authenticate_with_qr_code('1234', '1234', 'uuid')
        self.nu_transactions = self.nu.get_card_statements()

    def test_should_import_barcode_transactions_using_detail_as_payee(self):
        nu_credit_card = NubankCreditCardData(self.nu, 'some-id')

        nu_transaction = self.nu_transactions[0]
        imported_transaction = list(nu_credit_card.get_data())[0]

        self.assertEqual(imported_transaction['transaction_id'], nu_transaction['id'])
        self.assertEqual(imported_transaction['account_id'], 'some-id')
        self.assertEqual(imported_transaction['amount'], nu_transaction['amount'] * 10 * -1)
        self.assertEqual(imported_transaction['payee'], nu_transaction['description'])
        self.assertEqual(imported_transaction['date'], nu_transaction['time'][:10])

