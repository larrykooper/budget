from src.authorities.authority_finder import AuthorityFinder
from src.models.persistence.transaction_type import TransactionType

class TransactionTypeInputField:

    def what_to_persist(self, value):
        ttid = self.get_trans_type(value.lower())
        return {self.line_item_field_name(): ttid}

    def line_item_field_name(self):
        return "transaction_type_id"


    def get_trans_type(self, input_type):
        authority_finder = AuthorityFinder()
        trans_type = TransactionType(input_type)
        if trans_type.has_autotranslation():
            type_to_lookup = trans_type.autotranslation()
        else:
            type_to_lookup = input_type
        id = authority_finder.authority_lookup("transaction_type", type_to_lookup)
        if id:
            return id
        else:
            return TransactionType.id_for_unknown()

