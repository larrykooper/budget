from src.authorities.authority_finder import AuthorityFinder
from src.models.category import Category
from src.models.description import Description

class CategorySetter:

    def get_category(self, input_cat, description):
        authority_finder = AuthorityFinder()
        desc = Description(description)
        input_cat_obj = Category(input_cat)
        # See if there is a rule to determine the
        #  category given the description
        #  and if there is, look up the ID of that category
        category_found_by_rule = desc.category_by_rule()
        if category_found_by_rule:
            cat_to_lookup = category_found_by_rule
        else:   # If we haven't got the cat to lookup yet, it's the input_cat
            cat_to_lookup = input_cat
        id = authority_finder.authority_lookup("category", cat_to_lookup)
        if id:
            return id
        else:
            return Category.id_for_uncategorized()
