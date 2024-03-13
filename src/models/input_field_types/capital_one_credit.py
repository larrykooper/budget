from decimal import Decimal

from src.models.input_field_types.input_field import InputField
from src.models.input_field_types.transaction_type_input_field import TransactionTypeInputField

class CapitalOneCredit(InputField):

    # A CapitalOneCredit is an amount that Capital One identifies as a credit in its file
    # It is usually when I pay off that card
    # Its sign should be positive because it is something I spend
    #  Its transaction type should be credit_card_payment

    def what_to_persist(self, value):
        if value:
            amount_d = Decimal(value)
            trans = "credit_card_payment"
            # do lookup for transaction
            trans_type = TransactionTypeInputField()
            ttid = trans_type.get_trans_type(trans)
            return {"amount": amount_d, "transaction_type_id": ttid}
        return {}
