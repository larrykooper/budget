from src.models.account_types.account import Account

class CapitalOne(Account):

    def column_map(self):
        return {
            "Transaction Date": "TRANSACTION_DATE",
            "Posted Date": "CREDIT_CARD_POST_DATE",
            "Card No.": "DROP",
            "Description": "DESCRIPTION",
            "Category": "CATEGORY",
            "Debit": "CAPITAL_ONE_DEBIT",
            "Credit": "CAPITAL_ONE_CREDIT"
        }
