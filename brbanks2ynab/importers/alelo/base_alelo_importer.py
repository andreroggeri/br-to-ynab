import abc
import uuid
from datetime import datetime
from typing import Iterable

from python_alelo.alelo import Alelo

from brbanks2ynab.importers.data_importer import DataImporter
from brbanks2ynab.importers.transaction import Transaction
from brbanks2ynab.utils.exception import ImporterException


class BaseAleloImporter(DataImporter):

    def __init__(self, alelo: Alelo, account_id: str):
        self.alelo = alelo
        self.account_id = account_id
        self.cards = self.alelo.get_cards()

    @abc.abstractmethod
    def get_data(self) -> Iterable[Transaction]:
        pass

    def _get_card_by_type(self, card_type: str):
        card = next((card for card in self.cards if card.card_type == card_type), None)
        if card is None:
            raise ImporterException(f'Unexistent card type {card_type}')

        return card

    def _to_transaction(self, alelo_transaction: dict) -> Transaction:
        transaction_merged_data = f'{alelo_transaction["date"]}:{alelo_transaction["value"]}:{alelo_transaction["description"]}'
        transaction_id = str(uuid.uuid5(uuid.NAMESPACE_URL, transaction_merged_data))
        return {
            'transaction_id': transaction_id,
            'account_id': self.account_id,
            'payee': alelo_transaction['description'],
            'amount': self._format_amount(alelo_transaction['value'], alelo_transaction['type']),
            'date': self._format_date(alelo_transaction['date'])
        }

    def _format_date(self, date: str) -> str:
        current_year = datetime.now().year
        return datetime.strptime(date, '%d/%m').replace(year=current_year).strftime('%Y-%m-%d')

    def _format_amount(self, amount: float, type: str) -> int:
        if type == 'DEBIT':
            return int(amount * 100) * -1
        else:
            return int(amount * 100)
