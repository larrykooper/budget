from src.models.category import Category
from src.translation.category_rules import CategoryRules

class Description:

    def __init__(
        self, desc: str
    ):
        self.desc = desc

    def category_by_rule(self) -> Category:
        returnval = None
        desc = self.desc
        for rule in CategoryRules.starts_with_rules:
            if desc.startswith(rule['term']):
                returnval = rule['category']
                break
        if not returnval:
            for rule in CategoryRules.contains_rules:
                if rule['term'] in desc:
                    returnval = rule['category']
                    break
        return returnval

