from src.models.input_field_types.input_field import InputField

class TransactionDate(InputField):

    def what_to_persist(self, value):
        return {self.line_item_field_name(): value}

    def line_item_field_name(self):
        return "transaction_date"
