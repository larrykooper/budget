from psycopg import sql

from src.adapters.repositories.abstract_repository import AbstractRepository
import src.flask_app.database.db_pool as db_pool

class AuthorityRepository(AbstractRepository):

    def add_line_item(self, line_item):
        raise NotImplementedError

    def authority_lookup(self, table: str, name: str) -> int:
        """
        Used when ingesting bank data
        """
        qstring = """
            SELECT id FROM {}
            WHERE name = %(name)s
        """
        params = {'name': name}
        executable_sql = sql.SQL(qstring).format(sql.Identifier(table))
        data = db_pool.get_data(executable_sql, params, single_row=True)
        if data:
            return data['id']
        else:
            return None


    def authority_display(self, table: str, id: int) -> str:
        qstring = """
            SELECT name FROM {}
            WHERE id = %(id)s
        """
        params = {'id': id}
        executable_sql = sql.SQL(qstring).format(sql.Identifier(table))
        data = db_pool.get_data(executable_sql, params, single_row=True)
        return data['name']
