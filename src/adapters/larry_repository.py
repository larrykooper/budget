from src.adapters.abstract_repository import AbstractRepository
import src.adapters.mydb as mydb 


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
        VALUES (%s, %s, %s, %s, %s, %s, %s)          
        """
        values = (
            line_item.transaction_date, 
            line_item.post_date,   
            line_item.description,           
            line_item.amount, 
            line_item.category_id, 
            line_item.transaction_type_id,
            line_item.account_id
        )  
        with mydb.db_cursor() as cur:    
            cur.execute(query, values)


    def get(self, id):
        query = """
        SELECT * FROM line_item
        """
        with mydb.db_cursor() as cur:
            cur.execute(query)
