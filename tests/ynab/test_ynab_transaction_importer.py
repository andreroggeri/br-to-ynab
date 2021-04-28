import unittest
from datetime import datetime, timedelta
from typing import Iterable
from unittest.mock import Mock

from ynab_sdk import YNAB

from br_to_ynab.importers.data_importer import DataImporter
from br_to_ynab.importers.transaction import Transaction
from br_to_ynab.ynab.ynab_transaction_importer import YNABTransactionImporter

today = datetime.now()


class FakeImporter(DataImporter):

    def get_data(self) -> Iterable[Transaction]:
        return [
            {
                'transaction_id': '1',
                'account_id': 'some-id-one',
                'payee': 'Some Payee',
                'amount': 15000,
                'date': today.strftime('%Y-%m-%d'),
            },
            {
                'transaction_id': '2',
                'account_id': 'some-id-two',
                'payee': 'Some Mall',
                'amount': 99000,
                'date': (today - timedelta(weeks=54)).strftime('%Y-%m-%d'),
            }
        ]


class TestYNABTransactionImporter(unittest.TestCase):

    def test_should_import_transactions(self):
        fake_ynab = Mock(YNAB)
        start_date = (today - timedelta(weeks=4)).strftime('%Y-%m-%d')
        importer = YNABTransactionImporter(fake_ynab, '1234', start_date)

        importer.get_transactions_from(FakeImporter())
        importer.save()

        fake_ynab.transactions.create_transactions.assert_called_once()

    def test_should_ignore_transactions_past_start_date(self):
        fake_ynab = Mock(YNAB)
        start_date = (today - timedelta(weeks=4)).strftime('%Y-%m-%d')
        importer = YNABTransactionImporter(fake_ynab, '1234', start_date)

        importer.get_transactions_from(FakeImporter())

        self.assertEqual(len(importer.transactions), 1)
        self.assertEqual(importer.transactions[0].import_id, '1')

