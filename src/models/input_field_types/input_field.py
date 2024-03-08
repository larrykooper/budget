# An InputField is one field or column that is in the input from banks/CCs

class NoFieldTypeForInputField(Exception):
    def __init__(self, input_field):
        message = f"No field type for input field {input_field}"
        super().__init__(message)

class InputField:

    @staticmethod
    def instantiate_input_field(input_field):
        from src.models.input_field_types.amount_no_change import AmountNoChange
        from src.models.input_field_types.bank_amount import BankAmount
        from src.models.input_field_types.bank_description import BankDescription
        from src.models.input_field_types.bank_post_date import BankPostDate
        from src.models.input_field_types.capital_one_credit import CapitalOneCredit
        from src.models.input_field_types.capital_one_debit import CapitalOneDebit
        from src.models.input_field_types.category_input_field import CategoryInputField
        from src.models.input_field_types.chase_credit_card_amount import ChaseCreditCardAmount
        from src.models.input_field_types.check_number_input_field import CheckNumberInputField
        from src.models.input_field_types.credit_card_post_date import CreditCardPostDate
        from src.models.input_field_types.description_input_field import DescriptionInputField
        from src.models.input_field_types.transaction_date import TransactionDate
        from src.models.input_field_types.transaction_type_input_field import TransactionTypeInputField
        from src.models.input_field_types.type_detail_input_field import TypeDetailInputField
        if input_field == "AMOUNT_NO_CHANGE":
            return AmountNoChange()
        if input_field == "BANK_AMOUNT":
            return BankAmount()
        if input_field == "BANK_DESCRIPTION":
            return BankDescription()
        if input_field == "BANK_POST_DATE":
            return BankPostDate()
        if input_field == "CAPITAL_ONE_CREDIT":
            return CapitalOneCredit()
        if input_field == "CAPITAL_ONE_DEBIT":
            return CapitalOneDebit()
        if input_field == "CATEGORY":
            return CategoryInputField()
        if input_field == "CHASE_CREDIT_CARD_AMOUNT":
            return ChaseCreditCardAmount()
        if input_field == "CHECK_NUMBER":
            return CheckNumberInputField()
        if input_field == "CREDIT_CARD_POST_DATE":
            return CreditCardPostDate()
        if input_field == "DESCRIPTION":
            return DescriptionInputField()
        if input_field == "DETAILS":
            return TransactionTypeInputField()
        if input_field == "TRANSACTION_DATE":
            return TransactionDate()
        if input_field == "TRANSACTION_TYPE":
            return TransactionTypeInputField()
        if input_field == "TYPE_DETAIL":
            return TypeDetailInputField()
        raise NoFieldTypeForInputField(input_field)
        return None

    def what_to_persist(self, value):
        #return _type.what_to_persist()
        raise NotImplementedError
