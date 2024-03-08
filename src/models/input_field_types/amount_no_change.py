from decimal import Decimal

from src.models.input_field_types.input_field import InputField

# An Amount No Change is written out same as it is received
class AmountNoChange(InputField):

    def what_to_persist(self, value):
        amount_d = Decimal(value)
        return {self.line_item_field_name(): amount_d}

    def line_item_field_name(self):
        return "amount"


