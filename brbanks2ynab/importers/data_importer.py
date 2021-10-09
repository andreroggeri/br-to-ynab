import abc
from typing import Iterable

from brbanks2ynab.importers.transaction import Transaction


class DataImporter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self) -> Iterable[Transaction]:
        raise NotImplementedError
