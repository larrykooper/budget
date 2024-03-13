from src.models.input_field_types.category_input_field import CategoryInputField
from src.models.input_field_types.input_field import InputField


# A Bank Description is the contents of the Description field provided by the bank.
#  It's treated differently from the credit card description because it does not come
#  in with a category.
class BankDescription(InputField):

    def what_to_persist(self, value) -> dict:
        cat_field = CategoryInputField()
        category_id = cat_field.get_category_id("", value)
        return {"description": value, "category_id": category_id}
