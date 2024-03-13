from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.category_rule_repository import CategoryRuleRepository
from src.models.input_field_types.input_field import InputField
from src.models.category import Category


class CategoryInputField(InputField):

    def what_to_persist(self, value, description):
        cid = self.get_category_id(value, description)
        return {self.line_item_field_name(): cid}

    def line_item_field_name(self):
        return "category_id"

    def get_category_id(self, input_cat, description: str):
        authority_repo = AuthorityRepository()
        # See if there is a rule to determine the
        #  category given the description
        #  and if there is, look up the ID of that category
        category_id_found_by_rule = self.category_by_rule(description)
        if category_id_found_by_rule:
            return category_id_found_by_rule
        # If we haven't got the cat to lookup yet, it's the input_cat
        cat_to_lookup = input_cat
        id = authority_repo.authority_lookup("category", cat_to_lookup)
        if id:
            return id
        else:
            return Category.id_for_uncategorized()

    def category_by_rule(self, description: str):
        category_rule_repo = CategoryRuleRepository()
        # Convert description to lowercase
        desc_low = description.lower()
        # get_starts_with_rule uses LIKE 'foo%'
        starts_with_rule = category_rule_repo.get_starts_with_rule(desc_low)
        if starts_with_rule:
            return starts_with_rule['category_id']
        # get_contains_rule uses LIKE '%foo%'
        contains_rule = category_rule_repo.get_contains_rule(desc_low)
        if contains_rule:
            return contains_rule['category_id']
        return None


