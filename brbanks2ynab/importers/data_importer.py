import abc
from typing import Iterable

from brbanks2ynab.importers.transaction import Transaction


class DataImporter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    async def get_data(self) -> Iterable[Transaction]:
        raise NotImplementedError
