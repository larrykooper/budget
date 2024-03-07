from src.authorities.authority_finder import AuthorityFinder
from src.models.input_field_types.description_input_field import DescriptionInputField
from src.models.input_field_types.input_field import InputField
from src.models.persistence.category import Category
from src.translation.category_rules import CategoryRules


class CategoryInputField(InputField):

    def what_to_persist(self, value, description):
        cid = self.get_category_id(value, description)
        return {self.line_item_field_name(): cid}

    def line_item_field_name(self):
        return "category_id"

    def get_category_id(self, input_cat, description: str):
        authority_finder = AuthorityFinder()
        # See if there is a rule to determine the
        #  category given the description
        #  and if there is, look up the ID of that category
        category_found_by_rule = self.category_by_rule(description)
        if category_found_by_rule:
            cat_to_lookup = category_found_by_rule
        else:   # If we haven't got the cat to lookup yet, it's the input_cat
            cat_to_lookup = input_cat
        id = authority_finder.authority_lookup("category", cat_to_lookup)
        if id:
            return id
        else:
            return Category.id_for_uncategorized()


    def category_by_rule(self, description: str):
        returnval = None
        for rule in CategoryRules.starts_with_rules:
            if description.startswith(rule['term']):
                returnval = rule['category']
                break
        if not returnval:
            for rule in CategoryRules.contains_rules:
                if rule['term'] in description:
                    returnval = rule['category']
                    break
        return returnval


