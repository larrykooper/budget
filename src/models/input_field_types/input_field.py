# An InputField is one field or column that is in the input from banks/CCs

class InputField:

    @staticmethod
    def instantiate_input_field(input_field):
        from src.models.input_field_types.chase_credit_card_amount import ChaseCreditCardAmount
        from src.models.input_field_types.category_input_field import CategoryInputField
        from src.models.input_field_types.description_input_field import DescriptionInputField
        from src.models.input_field_types.post_date import PostDate
        from src.models.input_field_types.transaction_date import TransactionDate
        from src.models.input_field_types.transaction_type_input_field import TransactionTypeInputField
        if input_field == 'CATEGORY':
            return CategoryInputField()
        if input_field == 'CHASE_CREDIT_CARD_AMOUNT':
            return ChaseCreditCardAmount()
        if input_field == 'DESCRIPTION':
            return DescriptionInputField()
        if input_field == "POST_DATE":
            return PostDate()
        if input_field == "TRANSACTION_DATE":
            return TransactionDate()
        if input_field == 'TRANSACTION_TYPE':
            return TransactionTypeInputField()
        return None

    def what_to_persist(self, value):
        #return _type.what_to_persist()
        raise NotImplementedError
