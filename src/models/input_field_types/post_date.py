from src.models.input_field_types.input_field import InputField

class PostDate(InputField):

    def what_to_persist(self, value) -> dict:
        return {"post_date": value, "transaction_date": value}

