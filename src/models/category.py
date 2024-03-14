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


    def memoize(func):
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
    def categories_for_select():
        """
        Returns JSON in this form:
        With values sorted, not indices
        [{index:"57", value:"Bars"},
        {index:"2", value:"Birding"},
        {index:"4", value:"Books"},
        {index:"3", value:"Building Staff"} ]
        """
        #  create a list of dicts
        category_repo = CategoryRepository()
        cats = category_repo.get_all_categories()
        cats_list = []
        for cat in cats:
            d = {"index": cat['id'], "value": cat['name']}
            cats_list.append(d)
        return json.dumps(cats_list)

