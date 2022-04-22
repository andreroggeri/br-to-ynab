import json
import unittest
from pathlib import Path
from typing import Iterator
from unittest.mock import patch

from inquirer import events
from readchar import key

from brbanks2ynab.config.initialize import init_config

args = [
    'ynab_token',
    'ynab_budget',
    'banks',
    'start_import_date',
    'nubank_login',
    'nubank_token',
    'nubank_cert',
    'nubank_credit_card_account',
    'nubank_checking_account',
    'bradesco_branch',
    'bradesco_account_no',
    'bradesco_account_digit',
    'bradesco_web_password',
    'bradesco_credit_card_account',
    'bradesco_checking_account',
    'alelo_login',
    'alelo_password',
    'alelo_flex_account',
    'alelo_refeicao_account',
    'alelo_alimentacao_account',
]


class IterableEvent:
    def __init__(self, iterable: Iterator):
        self.iterator = iterable

    def next(self):
        return events.KeyPressed(next(self.iterator))


def add_text_input(value):
    result = list(value)
    result.append(key.ENTER)
    return result


def make_answers(readkey_mock, **kwargs):
    inputs = []

    for arg in args:
        in_data = kwargs.get(arg)
        if in_data:
            if isinstance(in_data, str):
                inputs.extend(add_text_input(in_data))
            elif isinstance(in_data, list):
                if 'Nubank' in in_data:
                    inputs.extend([key.SPACE])
                if 'Bradesco' in in_data:
                    inputs.extend([key.DOWN, key.SPACE])
                if 'Alelo' in in_data:
                    inputs.extend([key.DOWN, key.DOWN, key.SPACE])
                inputs.append(key.ENTER)

    readkey_mock.side_effect = inputs


class TestConfigInitialize(unittest.TestCase):

    def setUp(self) -> None:
        self.clean()

    def tearDown(self) -> None:
        self.clean()

    def clean(self):
        config_file = self.get_config_file()

        if config_file.exists():
            config_file.unlink()

    def get_config_file(self):
        pwd = Path()
        return pwd.joinpath('brbanks2ynab.json')

    @patch('readchar.readkey')
    def test_should_configure_nubank(self, readkey_mock):
        answers = {
            'ynab_token': 'abc-123',
            'ynab_budget': 'budget-name',
            'banks': ['Nubank'],
            'start_import_date': '2021-04-27',
            'nubank_login': '12345678912',
            'nubank_token': 'some-token',
            'nubank_cert': '/etc/hosts',
            'nubank_credit_card_account': 'Nubs',
            'nubank_checking_account': 'Nubs2'
        }
        make_answers(
            readkey_mock,
            **answers
        )

        init_config()

        config_file = self.get_config_file()

        self.assertTrue(config_file.exists())

        parsed = json.loads(config_file.read_text())
        answers.pop('nubank_cert')
        parsed.pop('nubank_cert')

        self.assertEqual(parsed, answers)

    @patch('readchar.readkey')
    def test_should_fail_configure_invalid_cert_path(self, readkey_mock):
        answers = {
            'ynab_token': 'abc-123',
            'ynab_budget': 'budget-name',
            'banks': ['Nubank'],
            'start_import_date': '2021-04-27',
            'nubank_login': '12345678912',
            'nubank_token': 'some-token',
            'nubank_cert': './fake-file.txt',
            'nubank_card_account': 'Nubs',
            'nubank_checking_account': 'Nubs2'
        }
        make_answers(
            readkey_mock,
            **answers
        )

        self.assertRaises(StopIteration, init_config)

        config_file = self.get_config_file()

        self.assertFalse(config_file.exists())

    @patch('readchar.readkey')
    def test_should_fail_init_with_invalid_start_date(self, readkey_mock):
        answers = {
            'ynab_token': 'abc-123',
            'ynab_budget': 'budget-name',
            'banks': ['Nubank'],
            'start_import_date': '202xx-04-27',
        }
        make_answers(
            readkey_mock,
            **answers
        )

        self.assertRaises(StopIteration, init_config)

        config_file = self.get_config_file()

        self.assertFalse(config_file.exists())

    @patch('readchar.readkey')
    def test_should_configure_bradesco(self, readkey_mock):
        answers = {
            'ynab_token': 'abc-123',
            'ynab_budget': 'budget-name',
            'banks': ['Bradesco'],
            'start_import_date': '2021-04-27',
            'bradesco_branch': '1234',
            'bradesco_account_no': '123123123',
            'bradesco_account_digit': '2',
            'bradesco_web_password': '1234',
            'bradesco_credit_card_account': 'Bradesco Visa',
            'bradesco_checking_account': 'Bradesco Corrente',
        }
        make_answers(
            readkey_mock,
            **answers
        )

        init_config()

        config_file = self.get_config_file()

        self.assertTrue(config_file.exists())

        parsed = json.loads(config_file.read_text())

        self.assertEqual(parsed, answers)

    @patch('readchar.readkey')
    def test_should_configure_alelo(self, readkey_mock):
        answers = {
            'ynab_token': 'abc-123',
            'ynab_budget': 'budget-name',
            'banks': ['Alelo'],
            'start_import_date': '2021-04-27',
            'alelo_login': '1234',
            'alelo_password': 'abc123',
            'alelo_flex_account': 'aaaa',
            'alelo_refeicao_account': 'bbbc',
            'alelo_alimentacao_account': 'cccc',
        }

        make_answers(
            readkey_mock,
            **answers
        )

        init_config()

        config_file = self.get_config_file()

        self.assertTrue(config_file.exists())

        parsed = json.loads(config_file.read_text())

        self.assertEqual(parsed, answers)


if __name__ == '__main__':
    unittest.main()
