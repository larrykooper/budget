from decimal import Decimal

from src.models.input_field_types.input_field import InputField
# A ChaseCreditCardAmount is an amount field from a Chase Credit Card bill

class ChaseCreditCardAmount(InputField):

    def what_to_persist(self, value):
        amount_d = Decimal(value)
        amount = -1 * amount_d
        return {self.line_item_field_name(): amount}

    def line_item_field_name(self):
        return "amount"


