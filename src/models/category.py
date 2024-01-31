from src.authorities.authority_finder import AuthorityFinder
from src.translation.category_autotranslation import CategoryAutotranslation

class Category:

    def __init__(
        self, name: str
    ):
        self.name = name

    def has_autotranslation(self):
        return self.name in CategoryAutotranslation.category_autotranslation
        

    def autotranslation(self):
        return CategoryAutotranslation.category_autotranslation[self.name]  

    @staticmethod
    def id_for_uncategorized():
        authority_finder = AuthorityFinder()
        return authority_finder.authority_lookup("category", "Uncategorized")  
