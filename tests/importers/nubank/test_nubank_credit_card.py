import uuid

import pytest
from pynubank import Nubank, MockHttpClient

from brbanks2ynab.importers.nubank.nubank_credit_card import NubankCreditCardData


def build_card_transaction(overrides: dict) -> dict:
    default_transaction = {
        'id': str(uuid.uuid4()),
        'amount': 1000,
        'description': 'Some description',
        'time': '2021-01-01',
        'details': {
            'status': 'settled'
        }
    }
    
    return {
        **default_transaction,
        **overrides
    }


@pytest.fixture
def setup_nubank():
    nu = Nubank(client=MockHttpClient())
    nu.authenticate_with_qr_code('1234', '1234', 'uuid')
    return nu


def test_should_only_import_settled_transactions(setup_nubank, monkeypatch):
    nu = setup_nubank
    to_be_imported = build_card_transaction({'details': {'status': 'settled'}, 'amount': 1000})
    transactions = [
        to_be_imported,
        build_card_transaction({'details': {'status': 'unsettled'}}),
    ]
    monkeypatch.setattr(nu, 'get_card_statements', lambda: transactions)
    nu_credit_card = NubankCreditCardData(nu, 'some-id')
    
    result = list(nu_credit_card.get_data())
    
    assert len(result) == 1
    
    imported = result[0]
    
    assert imported == {
        'account_id': 'some-id',
        'transaction_id': to_be_imported['id'],
        'date': to_be_imported['time'],
        'amount': -10000,
        'payee': to_be_imported['description'],
        'flag': None,
        'memo': '',
    }


def test_should_expand_installment_transactions(setup_nubank, monkeypatch):
    nu = setup_nubank
    installment_transaction = build_card_transaction({
        'amount': 3000,
        'details': {
            'status': 'settled',
            'charges': {
                'count': 3,
                'amount': 1000
            }
        }
    })
    regular_transaction = build_card_transaction({'amount': 3000})
    transactions = [
        regular_transaction,
        installment_transaction
    ]
    monkeypatch.setattr(nu, 'get_card_statements', lambda: transactions)
    
    importer = NubankCreditCardData(nu, 'some-id')
    imported_transactions = list(importer.get_data())
    
    ids = list(map(lambda x: x['transaction_id'], imported_transactions))
    
    assert len(imported_transactions) == 4
    assert imported_transactions[0]['amount'] == -30000
    assert imported_transactions[1]['memo'] == 'Parcela 1 de 3. Valor total: R$ 30,00'
    assert imported_transactions[1]['flag'] == 'red'
    assert imported_transactions[1]['amount'] == -10000
    assert imported_transactions[2]['memo'] == 'Parcela 2 de 3. Valor total: R$ 30,00'
    assert imported_transactions[2]['flag'] == 'red'
    assert imported_transactions[2]['amount'] == -10000
    assert imported_transactions[3]['memo'] == 'Parcela 3 de 3. Valor total: R$ 30,00'
    assert imported_transactions[3]['flag'] == 'red'
    assert imported_transactions[3]['amount'] == -10000
    # All ids should be unique
    assert len(ids) == len(set(ids))
    


def test_should_not_expand_transactions_with_one_installment(setup_nubank, monkeypatch):
    nu = setup_nubank
    installment_transaction = build_card_transaction({
        'amount': 3000,
        'details': {
            'status': 'settled',
            'charges': {
                'count': 1,
                'amount': 3000
            }
        }
    })
    transactions = [
        installment_transaction
    ]
    monkeypatch.setattr(nu, 'get_card_statements', lambda: transactions)
    
    importer = NubankCreditCardData(nu, 'some-id')
    imported_transactions = list(importer.get_data())
    
    assert len(imported_transactions) == 1
    assert imported_transactions[0]['amount'] == -30000
    assert imported_transactions[0]['memo'] == ''
    assert imported_transactions[0]['flag'] is None


def test_should_set_the_day_to_first_for_following_installments(setup_nubank, monkeypatch):
    nu = setup_nubank
    installment_transaction = build_card_transaction({
        'amount': 3000,
        'time': '2021-01-15',
        'details': {
            'status': 'settled',
            'charges': {
                'count': 3,
                'amount': 1000
            }
        }
    })
    transactions = [
        installment_transaction
    ]
    monkeypatch.setattr(nu, 'get_card_statements', lambda: transactions)
    
    importer = NubankCreditCardData(nu, 'some-id')
    imported_transactions = list(importer.get_data())
    
    assert len(imported_transactions) == 3
    assert imported_transactions[0]['date'] == '2021-01-15'
    assert imported_transactions[1]['date'] == '2021-02-01'
    assert imported_transactions[2]['date'] == '2021-03-01'
