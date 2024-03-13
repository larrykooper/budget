from src.models.account_types.account import Account

class Discover(Account):

    def column_map(self):
        return {
            "Trans. Date": "TRANSACTION_DATE",
            "Post Date": "CREDIT_CARD_POST_DATE",
            "Description": "DESCRIPTION",
            "Amount": "AMOUNT_NO_CHANGE",
            "Category": "CATEGORY"
        }
