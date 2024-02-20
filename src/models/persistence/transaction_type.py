from src.authorities.authority_finder import AuthorityFinder
from src.translation.transaction_type_autotranslation import TransactionTypeAutotranslation

class TransactionType: 

    def __init__(
        self, name: str
    ):
        self.name = name

    def has_autotranslation(self):
        return self.name in TransactionTypeAutotranslation.trans_type_autotranslation
    
    def autotranslation(self):
        return TransactionTypeAutotranslation.trans_type_autotranslation[self.name]


    @staticmethod
    def id_for_unknown():
        authority_finder = AuthorityFinder()
        return authority_finder.authority_lookup("transaction_type", "unknown")    
