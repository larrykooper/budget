from src.adapters.repositories.abstract_repository import AbstractRepository
import src.flask_app.database.db_pool as db_pool

class CategoryRepository(AbstractRepository):
    # INSERT

    def add_line_item(self, line_item):
        raise NotImplementedError

    # SELECT

    def get_all_categories(self) -> list[dict]:
        query = """
        SELECT id, name, budget_per_month FROM category
        ORDER BY name
        """
        params = {}
        data = db_pool.get_data(query, params, single_row=False)
        return data

   # UPDATE

    def update_budget_per_month(self, new_value, id):
        query = """
        UPDATE category
        SET budget_per_month = %(new_value)s
        WHERE id = %(category_id)s
        """
        params = {
            'new_value': new_value,
            'category_id': id
        }
        db_pool.update(query, params)

