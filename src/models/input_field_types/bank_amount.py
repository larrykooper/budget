from decimal import Decimal

from src.models.input_field_types.input_field import InputField
# A BankAmount is the Amount from the Bank file type

class BankAmount(InputField):

    def what_to_persist(self, value):
        amount_d = Decimal(value)
        amount = abs(amount_d)
        return {self.line_item_field_name(): amount}

    def line_item_field_name(self):
        return "amount"

