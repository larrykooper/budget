from src.adapters.repositories.abstract_repository import AbstractRepository
import src.flask_app.database.db_pool as db_pool

class CategoryRuleRepository(AbstractRepository):

    def add_line_item(self, line_item):
        raise NotImplementedError

    # INSERT

    def add_categorization_rule(self, category_rule):
        query = """
        INSERT INTO category_rule (
            term,
            rule_type_id,
            category_id
        )
        VALUES (%(term)s, %(rule_type_id)s, %(category_id)s);
        """
        params = {
            'term': category_rule.term,
            'rule_type_id': category_rule.rule_type_id,
            'category_id': category_rule.category_id
        }
        results = db_pool.insert(query, params)
        # Results is "True" if it's OK
        return results

    # SELECT

    def get_starts_with_rule(self, desc_low: str) -> str:
        qstring = """
        SELECT category
        FROM category_rule crule
        INNER JOIN rule_type rt
        ON crule.rule_type_id = rt.id
        WHERE rt.name = 'starts_with'
        AND %(desc_low)s LIKE term || '%%'
        """
        params = {
            'desc_low': desc_low
        }
        data = db_pool.get_data(qstring, params, single_row=True)
        return data

    """
    this works, for get_starts_with_rule:

        SELECT category
        FROM category_rule
        WHERE rule_type_id = 2
        AND 'starbucks store 15685' LIKE term || '%'

    """

    def get_contains_rule(self, desc_low: str) -> str:
        qstring = """
        SELECT category
        FROM category_rule crule
        INNER JOIN rule_type rt
        ON crule.rule_type_id = rt.id
        WHERE rt.name = 'contains'
        AND %(desc_low)s LIKE '%%' || term || '%%'
        """
        params = {
            'desc_low': desc_low
        }
        data = db_pool.get_data(qstring, params, single_row=True)
        return data

