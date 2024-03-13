from src.models.account_types.account import Account

class Amazon(Account):

    def column_map(self):
        return {
            "Transaction Date": "TRANSACTION_DATE",
            "Post Date": "CREDIT_CARD_POST_DATE",
            "Description": "DESCRIPTION",
            "Category": "CATEGORY",
            "Type": "TRANSACTION_TYPE",
            "Amount": "CHASE_CREDIT_CARD_AMOUNT",
            "Memo": "DROP"
        }
