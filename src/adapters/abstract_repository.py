import abc
from src.models.line_item import LineItem

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, line_item: LineItem):
        raise NotImplementedError

    @abc.abstractmethod
    def get(self) -> list:
        raise NotImplementedError