import json

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder

class Category:

    def __init__(
        self, name: str
    ):
        self.name = name

    @staticmethod
    def id_for_uncategorized():
        authority_finder = AuthorityFinder()
        return authority_finder.authority_lookup("category", "Uncategorized")

    def memoize(func):
        cache = {}

        def wrapper(*args):
            if args in cache:
                return cache[args]
            else:
                result = func(*args)
                cache[args] = result
                return result

        return wrapper

    @staticmethod
    @memoize
    def categories_json():
        repo = LarryRepository()
        cats = repo.get_all_categories()
        cats_dict = {}
        for cat in cats:
            cats_dict.update({cat['id']: cat['name']})
        return json.dumps(cats_dict)



