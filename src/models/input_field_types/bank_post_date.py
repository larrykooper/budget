from src.models.input_field_types.input_field import InputField

# Bank doesn't tell you transaction date so I use the post date for both
class BankPostDate(InputField):

    def what_to_persist(self, value) -> dict:
        return {"post_date": value, "transaction_date": value}
