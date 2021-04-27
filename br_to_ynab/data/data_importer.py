import abc
from typing import Iterable

from br_to_ynab.data.transaction import Transaction


class DataImporter(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def get_data(self) -> Iterable[Transaction]:
        raise NotImplementedError
