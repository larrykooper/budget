from src.adapters.abstract_repository import AbstractRepository
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
        VALUES (%(transaction_date)s, %(post_date)s, %(description)s, %(amount)s, %(category_id)s, %(transaction_type_id)s, %(account_id)s)          
        """
        params = {
            'transaction_date': line_item.transaction_date, 
            'post_date': line_item.post_date,   
            'description':line_item.description,           
            'amount': line_item.amount, 
            'category_id': line_item.category_id, 
            'transaction_type_id': line_item.transaction_type_id,
            'account_id': line_item.account_id
        }
        results = db_pool.insert(query, params)
        return results      


    def get(self):
        query = """
        SELECT * FROM line_item
        """
        params = {}
        data = db_pool.get_data(query, params, single_row=False)
        return data 
