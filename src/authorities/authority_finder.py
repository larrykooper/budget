import src.adapters.mydb as mydb 

class AuthorityFinder:

    def authority_lookup(self, table: str, name: str) -> int:
        query = f"""
            SELECT id FROM {table}
            WHERE name = %s
        """
        values = (name, )
        with mydb.db_cursor() as cur:    
            cur.execute(query, values)
            result = cur.fetchone()            
        return result[0] 


