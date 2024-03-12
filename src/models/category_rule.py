# A CategoryRule tells the system to pick a category
#  for a LineItem based on its description.
class CategoryRule:

    def __init__(
        self,
        term: str,
        category_id: int,
        rule_type_id: int
    ):
        self.term = term
        self.category_id = category_id
        self.rule_type_id = rule_type_id