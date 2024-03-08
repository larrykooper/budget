from src.models.account_types.account import Account

class ChaseChecking(Account):

    def column_map(self):
        return {
            "Details": "DETAILS",  # must lowercase it and then look it up
            "Posting Date": "BANK_POST_DATE", # copy to transo date
            "Description": "BANK_DESCRIPTION",  # I need to find a category for it
            "Amount": "BANK_AMOUNT",  # must take the absolute value
            "Type": "TYPE_DETAIL",  # authority
            "Balance": "DROP",
            "Check or Slip #": "CHECK_NUMBER"
        }