from src.authorities.authority_finder import AuthorityFinder
from src.models.category import Category
from src.models.description import Description

class CategorySetter:

    def get_category(self, input_cat, description):
        authority_finder = AuthorityFinder()
        desc = Description(description)
        input_cat_obj = Category(input_cat)
        if desc.has_description_autocat(): 
            cat_to_lookup = desc.autocat() 
        elif input_cat_obj.has_autotranslation():
            cat_to_lookup = input_cat_obj.autotranslation() 
        else:
            cat_to_lookup = input_cat     
        id = authority_finder.authority_lookup("category", cat_to_lookup)
        if id:
            return id 
        else: 
            return Category.id_for_uncategorized()

       