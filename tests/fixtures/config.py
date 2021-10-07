import pytest


@pytest.fixture
def config_for_nubank():
    return {
        "ynab_token": "abc-123",
        "ynab_budget": "budget-name",
        "banks": [
            "Nubank"
        ],
        "start_import_date": "2021-04-27",
        "nubank_login": "12345678912",
        "nubank_token": "some-token",
        "nubank_cert": "IyMKIyBIb3N0IERhdGFiYXNlCiMKIyBsb2NhbGhvc3QgaXMgdXNlZCB0byBjb25maWd1cmUgdGhlIGxvb3BiYWNrIGludGVyZmFjZQojIHdoZW4gdGhlIHN5c3RlbSBpcyBib290aW5nLiAgRG8gbm90IGNoYW5nZSB0aGlzIGVudHJ5LgojIwoxMjcuMC4wLjEJbG9jYWxob3N0CjI1NS4yNTUuMjU1LjI1NQlicm9hZGNhc3Rob3N0Cjo6MSAgICAgICAgICAgICBsb2NhbGhvc3QKCjE3Mi4yNy4yMTYuMTAyCWFwaWhtbC5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi4xMTcJc29uYXJwb3J0b3ByZC5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi4xMTgJc29uYXJwb3J0b2htbAoxNzIuMjcuMjE2LjExOCAgc29uYXJwb3J0b2htbC5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi43NglnaXRwb3J0b3ByZC5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi4xMzcJb2NwbWFzdGVyLnBvcnRvc2VndXJvLmJyYXNpbAoxNzIuMjcuMjEyLjE0Nglwb3J0b3NlbmhhLnBvcnRvc2VndXJvLmJyYXNpbAoxNzIuMjcuMjA0LjEwCW5leHVzcmVwby5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi43OQluZXh1c3BvcnRvcHJkCjE3Mi4yNy4yMTYuODEJamVua2luc3BvcnRvaG1sLnBvcnRvc2VndXJvLmJyYXNpbAoxNzIuMjcuMjE2LjIyNwlqZW5raW5zY2lwb3J0b3ByZC5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi4yMjcJamVua2luc3BvcnRvcHJkCjE3Mi4yNy4yMTYuNzkJbmV4dXNwb3J0b3ByZC5wb3J0b3NlZ3Vyby5icmFzaWwKMTcyLjI3LjIxNi43OAluZXh1c3BvcnRvaG1sLnBvcnRvc2VndXJvLmJyYXNpbAoxNzIuMjcuMjAyLjIxNglhZGZzLnBvcnRvc2VndXJvLmNvbS5icgoxNzIuMjcuMjE2LjcyCWdyZWdobWwKMTcyLjI3LjIxNi43MQlncmVnCjE3Mi4yNy4yMTYuNTYgICBncmFmYW5hCjE3Mi4yNy4yMTIuMTI4ICBhcGFjaGVobWxyZQoxNzIuMjcuMjEyLjEwNyAgYXBhY2hlaG1sMnJlCjE3Mi4yNy4yMTYuMTUgICBvdGRpZ2hvbW0ucG9ydG9zZWd1cm8uYnJhc2lsCjE3Mi4yNy4yMDQuMTE4ICBvc2JobWxhdXRvLnBvcnRvc2VndXJvLmJyYXNpbAoKIyBBZGRlZCBieSBEb2NrZXIgRGVza3RvcAojIFRvIGFsbG93IHRoZSBzYW1lIGt1YmUgY29udGV4dCB0byB3b3JrIG9uIHRoZSBob3N0IGFuZCB0aGUgY29udGFpbmVyOgoxMjcuMC4wLjEga3ViZXJuZXRlcy5kb2NrZXIuaW50ZXJuYWwKIyBFbmQgb2Ygc2VjdGlvbgo=",
        "nubank_credit_card_account": "Nubs",
        "nubank_checking_account": "Nubs2"
    }


@pytest.fixture
def config_for_bradesco():
    return {
        "ynab_token": "abc-123",
        "ynab_budget": "budget-name",
        "banks": [
            "Bradesco"
        ],
        "start_import_date": "2021-04-27",
        "bradesco_branch": "123",
        "bradesco_account_no": "456789",
        "bradesco_account_digit": "9",
        "bradesco_web_password": "5566",
        "bradesco_credit_card_account": "Visa",
        "bradesco_checking_account": "Conta Conta COrrente"
    }


@pytest.fixture
def config_for_alelo():
    return {
        'ynab_token': 'abc-123',
        'ynab_budget': 'budget-name',
        'banks': ['Alelo'],
        'start_import_date': '2021-04-27',
        'login': '1234',
        'alelo_password': 'abc123',
        'alelo_flex_account': 'aaaa',
        'alelo_refeicao_account': 'bbbc',
        'alelo_alimentacao_account': 'cccc',
    }
