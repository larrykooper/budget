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
