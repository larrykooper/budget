from decimal import Decimal

from src.models.input_field_types.input_field import InputField
from src.models.input_field_types.transaction_type_input_field import TransactionTypeInputField

# A CapitalOneDebit is an amount that Capital One identifies as a debit in its file
# Its sign needs to be positive because spending is positive in my system.
# And it's already positive so I can accept it as-is.
#  Its transaction type should be "debit"
class CapitalOneDebit(InputField):

    def what_to_persist(self, value):
        if value:
            amount_d = Decimal(value)
            trans = "debit"
            # do lookup for transaction
            trans_type = TransactionTypeInputField()
            ttid = trans_type.get_trans_type(trans)
            return {"amount": amount_d, "transaction_type_id": ttid}
        return {}
