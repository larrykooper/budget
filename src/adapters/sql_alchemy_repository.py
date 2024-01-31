from src.adapters.abstract_repository import AbstractRepository
from src.models.line_item import LineItem

"""
The "session" refers to the SQLAlchemy database session.
For explanation see:
https://docs.sqlalchemy.org/en/20/orm/session_basics.html
"""


class SqlAlchemyRepository(AbstractRepository):
    def __init__(self, session):
        self.session = session

    def add(self, line_item):
        self.session.add(line_item)

    def get(self, id):
        return self.session.query(LineItem).filter_by(id=id).one()

    def list(self):
        return self.session.query(LineItem).all()