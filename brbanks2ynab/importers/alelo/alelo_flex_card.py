from typing import Iterable

from python_alelo.alelo import TransactionsTime

from brbanks2ynab.importers.alelo.base_alelo_importer import BaseAleloImporter
from brbanks2ynab.importers.transaction import Transaction


class AleloFlexImporter(BaseAleloImporter):
    async def get_data(self) -> Iterable[Transaction]:
        card = self._get_card_by_type('FLEX')
        response = self.alelo.get_transactions(card, TransactionsTime.LAST_THREE_MONTHS)

        return map(self._to_transaction, response['transactions'])
