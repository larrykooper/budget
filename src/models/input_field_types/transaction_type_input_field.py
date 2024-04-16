from src.adapters.repositories.authority_repository import AuthorityRepository
from src.models.transaction_type import TransactionType

class TransactionTypeInputField:

    def what_to_persist(self, value):
        # I lowercase the value so it will match the authority table
        ttid = self.get_trans_type(value.lower())
        return {self.line_item_field_name(): ttid}

    def line_item_field_name(self):
        return "transaction_type_id"


    def get_trans_type(self, input_type):
        authority_repo = AuthorityRepository()
        trans_type = TransactionType(input_type)
        if trans_type.has_autotranslation():
            type_to_lookup = trans_type.autotranslation()
        else:
            type_to_lookup = input_type
        ttid = authority_repo.authority_lookup("transaction_type", type_to_lookup)
        if ttid:
            return ttid
        return TransactionType.id_for_unknown()
