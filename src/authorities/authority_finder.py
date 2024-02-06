import src.flask_app.database.db_pool as db_pool 

class AuthorityFinder:    

    def authority_lookup(self, table: str, name: str) -> int:
        """
        Used when ingesting bank data
        """
        query = f"""
            SELECT id FROM {table}
            WHERE name = %(name)s
        """
        params = {'name': name}
        data = db_pool.get_data(query, params, single_row=True)
        return data 
    
    def authority_display(self, table: str, id: int) -> str:
        query = f"""
            SELECT name FROM {table}
            WHERE id = %(id)s
        """
        params = {'id': id} 
        data = db_pool.get_data(query, params, single_row=True)
        return data['name']    

