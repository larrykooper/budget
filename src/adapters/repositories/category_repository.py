from src.adapters.repositories.abstract_repository import AbstractRepository
import src.flask_app.database.db_pool as db_pool

class CategoryRepository(AbstractRepository):

    def get_all_categories(self) -> list[dict]:
        query = """
        SELECT id, name, budget_per_month FROM category
        ORDER BY name
        """
        params = {}
        data = db_pool.get_data(query, params, single_row=False)
        return data

    def add_line_item(self, line_item):
        raise NotImplementedError