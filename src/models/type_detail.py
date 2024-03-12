from src.adapters.repositories.authority_repository import AuthorityRepository

# A TypeDetail is the more specific transaction type that the bank reports
class TypeDetail:

    def __init__(
        self, name: str
    ):
        self.name = name

    # no autotranslation, just lower case it

    @staticmethod
    def id_for_unknown():
        authority_repo = AuthorityRepository()
        return authority_repo.authority_lookup("transaction_type", "unknown")
