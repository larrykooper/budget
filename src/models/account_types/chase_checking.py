from src.models.account_types.account import Account

class ChaseChecking(Account):

    def column_map(self):
        return {
            "Details": "DETAILS",  # must lowercase it
            "Posting Date": "POST_DATE",
            "Description": "DESCRIPTION",
            "Amount": "BANK_AMOUNT",  # must take the absolute value
            "Type": "TYPE_DETAIL",  # authority
            "Balance": "DROP",
            "Check or Slip #": "check_number"
        }