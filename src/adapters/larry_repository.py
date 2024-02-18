import psycopg_pool
import psycopg
from decimal import Decimal
from src.adapters.abstract_repository import AbstractRepository
import src.adapters.config as config
import src.flask_app.database.db_pool as db_pool

class LarryRepository(AbstractRepository):

    def add(self, line_item):

        query = """
        INSERT INTO line_item (
            transaction_date,
            post_date,
            description,
            amount,
            category_id,
            transaction_type_id,
            account_id
        )
            VALUES (%(transaction_date)s, %(post_date)s, %(description)s, %(amount)s, %(category_id)s, %(transaction_type_id)s, %(account_id)s);
        """
        params = {
            'transaction_date': line_item.transaction_date,
            'post_date': line_item.post_date,
            'description': line_item.description,
            'amount': line_item.amount,
            'category_id': line_item.category_id,
            'transaction_type_id': line_item.transaction_type_id,
            'account_id': line_item.account_id
        }
        results = db_pool.insert(query, params)
        return results


    def get(self) -> list[dict]:
        # TODO select has to be restricted by the time range of the report
        #  almost always one calendar month
        query = """
        SELECT * FROM line_item
        ORDER BY transaction_date
        """
        params = {}
        data = db_pool.get_data(query, params, single_row=False)
        return data


    def get_all_categories(self) -> list[dict]:
        query = """
        SELECT id, name FROM category
        ORDER BY name
        """
        params = {}
        data = db_pool.get_data(query, params, single_row=False)
        return data

    def update_comment(self, new_value, id):
        query = """
        UPDATE line_item
        SET comment = %(new_value)s
        WHERE id = %(line_item_id)s
        """
        params = {
            'new_value': new_value,
            'line_item_id': id
        }
        db_pool.update(query, params)

    def update_category(self, new_value, id):
        query = """
        UPDATE line_item
        SET category_id = %(new_value)s
        WHERE id = %(line_item_id)s
        """
        params = {
            'new_value': new_value,
            'line_item_id': id
        }
        db_pool.update(query, params)

    def delete_line_item(self, id):
        query = """
        DELETE FROM line_item
        WHERE id = %(line_item_id)s
        """
        params = {
            'line_item_id': id
        }
        db_pool.delete(query, params)