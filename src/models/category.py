import json

from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.category_repository import CategoryRepository

class Category:

    def __init__(
        self, name: str
    ):
        self.name = name

    @staticmethod
    def id_for_uncategorized():
        authority_repo = AuthorityRepository()
        return authority_repo.authority_lookup("category", "Uncategorized")

    def memoize(self, func):
        cache = {}

        def wrapper(*args):
            if args in cache:
                return cache[args]
            result = func(*args)
            cache[args] = result
            return result

        return wrapper

    @staticmethod
    @memoize
    def categories_json():
        category_repo = CategoryRepository()
        cats = category_repo.get_all_categories()
        cats_dict = {}
        for cat in cats:
            cats_dict.update({cat['id']: cat['name']})
        return json.dumps(cats_dict)
