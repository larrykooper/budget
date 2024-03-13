import datetime

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

    def get_for_budyear(
            self,
            start_of_year: datetime.date,
            end_of_year: datetime.date
        ) -> list[dict]:
        """
        Get data for the budget by year report
        """
        query = """
        WITH spending_by_cat AS (
            SELECT DISTINCT category_id, EXTRACT(MONTH FROM transaction_date) AS mymonth,
            SUM(amount) OVER (PARTITION BY EXTRACT(MONTH FROM transaction_date), category_id)
            FROM line_item
            WHERE transaction_date BETWEEN %(start_of_year)s AND %(end_of_year)s
            AND show_on_spending_report
            ORDER BY category_id, mymonth
        )
        SELECT name,
        budget_per_month,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=1) AS spend_jan,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=2) AS spend_feb,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=3) AS spend_mar,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=4) AS spend_apr,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=5) AS spend_may,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=6) AS spend_jun,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=7) AS spend_jul,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=8) AS spend_aug,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=9) AS spend_sep,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=10) AS spend_oct,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=11) AS spend_nov,
        (SELECT sum FROM spending_by_cat WHERE category_id = category.id AND mymonth=12) AS spend_dec
        FROM category
        ORDER BY name
        """
        params = {
            'start_of_year': start_of_year,
            'end_of_year': end_of_year
        }
        data = db_pool.get_data(query, params, single_row=False)
        return data

    def get_total_budget(self):
        query = """
        SELECT sum(budget_per_month) FROM category
        """
        params = {}
        data = db_pool.get_data(query, params, single_row=True)
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

