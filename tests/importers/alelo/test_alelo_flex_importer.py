import unittest
from unittest.mock import Mock

import pytest
from python_alelo.alelo import Alelo, Card

from brbanks2ynab.utils.exception import ImporterException
from brbanks2ynab.importers.alelo.alelo_flex_card import AleloFlexImporter


@pytest.fixture
def fake_transactions():
    return [
        {
            "date": "04/10",
            "value": 138.65,
            "moneyType": "R$",
            "type": "DEBIT",
            "icon": "shopping",
            "description": "MERCADO DO ZE",
            "virtualCard": False
        },
        {
            "date": "04/10",
            "value": 319.51,
            "moneyType": "R$",
            "type": "DEBIT",
            "icon": "shopping",
            "description": "PAULISTAO",
            "virtualCard": False
        },
        {
            "date": "04/10",
            "value": 150.21,
            "moneyType": "R$",
            "type": "CREDIT",
            "icon": "shopping",
            "description": "Disponibilização do Beneficio",
            "virtualCard": False
        }
    ]


@pytest.fixture
def fake_card():
    return Card({
        'name': 'Flex',
        'type': 'FLEX',
        'lastNumbers': '1234',
        'id': 1234,
    })


def test_should_import_flex_transactions(fake_card, fake_transactions):
    fake_alelo = Mock(Alelo)
    fake_alelo.get_cards.return_value = [fake_card]
    fake_alelo.get_transactions.return_value = {'transactions': fake_transactions}
    importer = AleloFlexImporter(fake_alelo, '5555')

    transactions = list(importer.get_data())

    assert len(transactions) == len(fake_transactions)
    for i in range(len(fake_transactions)):
        assert transactions[i]['account_id'] == '5555'
        assert transactions[i]['payee'] == fake_transactions[i]['description']

    assert transactions[0]['amount'] == -138650
    assert transactions[1]['amount'] == -319510
    assert transactions[2]['amount'] == 150210


def test_should_raise_exception_if_flex_card_doesnt_exists(fake_card):
    fake_alelo = Mock(Alelo)
    fake_alelo.get_cards.return_value = []
    importer = AleloFlexImporter(fake_alelo, '5555')

    with pytest.raises(ImporterException) as ex:
        importer.get_data()
        assert isinstance(ex, ImporterException)


if __name__ == '__main__':
    unittest.main()
