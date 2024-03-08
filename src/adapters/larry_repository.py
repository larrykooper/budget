import datetime
import pytz


from src.adapters.abstract_repository import AbstractRepository
import src.flask_app.database.db_pool as db_pool

class LarryRepository(AbstractRepository):

    def add(self, line_item):

        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))

        query = """
        INSERT INTO line_item (
            transaction_date,
            post_date,
            description,
            amount,
            category_id,
            transaction_type_id,
            account_id,
            check_number,
            type_detail_id,
            created,
            updated
        )
            VALUES (%(transaction_date)s, %(post_date)s, %(description)s, %(amount)s,
              %(category_id)s, %(transaction_type_id)s, %(account_id)s, %(check_number)s, %(type_detail_id)s, %(created)s, %(updated)s);
        """
        params = {
            'transaction_date': line_item.transaction_date,
            'post_date': line_item.post_date,
            'description': line_item.description,
            'amount': line_item.amount,
            'category_id': line_item.category_id,
            'transaction_type_id': line_item.transaction_type_id,
            'account_id': line_item.account_id,
            'check_number': line_item.check_number,
            'type_detail_id': line_item.type_detail_id,
            'created': current_time,
            'updated': current_time

        }
        results = db_pool.insert(query, params)
        return results

    def get(self) -> list:
        raise NotImplementedError


    def get_by_date_range(self, start_date: datetime.date, end_date: datetime.date) -> list[dict]:
        query = """
        SELECT * FROM line_item
        WHERE transaction_date BETWEEN %(start_date)s AND %(end_date)s
        ORDER BY transaction_date
        """
        params = {
            'start_date': start_date,
            'end_date': end_date
        }
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
        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))
        query = """
        UPDATE line_item
        SET comment = %(new_value)s,
        updated = %(time)s
        WHERE id = %(line_item_id)s
        """
        params = {
            'new_value': new_value,
            'line_item_id': id,
            'time': current_time
        }
        db_pool.update(query, params)

    def update_category(self, new_value, id):
        current_time = datetime.datetime.now(pytz.timezone("America/New_York"))
        query = """
        UPDATE line_item
        SET category_id = %(new_value)s,
        updated = %(time)s
        WHERE id = %(line_item_id)s
        """
        params = {
            'new_value': new_value,
            'line_item_id': id,
            'time': current_time
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