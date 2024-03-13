import abc
from src.models.line_item import LineItem

class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add_line_item(self, line_item: LineItem):
        raise NotImplementedError

