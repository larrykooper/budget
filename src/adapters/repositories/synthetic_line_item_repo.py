import src.flask_app.database.db_pool as db_pool

class SyntheticLineItemRepo():

    def add_synthetic_line_item(self, synthetic_line_item):
        query = """
        INSERT INTO synthetic_line_item (
            line_item_id,
            deposit_based_on
        )
        VALUES (
            %(line_item_id)s,
            %(deposit_based_on)s
        );
        """
        params = {
            'line_item_id': synthetic_line_item.line_item_id,
            'deposit_based_on': synthetic_line_item.deposit_based_on
        }
        results = db_pool.insert(query, params)
        return results
