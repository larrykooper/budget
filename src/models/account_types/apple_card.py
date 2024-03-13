from src.models.account_types.account import Account

class AppleCard(Account):

    def column_map(self):
        return {
            "Transaction Date": "TRANSACTION_DATE",
            "Clearing Date": "CREDIT_CARD_POST_DATE",
            "Description": "DESCRIPTION",
            "Merchant": "DROP",
            "Category": "CATEGORY",
            "Type": "TRANSACTION_TYPE",
            "Amount (USD)": "AMOUNT_NO_CHANGE",
            "Purchased By": "DROP"
        }
