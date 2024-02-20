class ColumnMap:

#  map from: map to

    chase_cc_map = {
        "Transaction Date": "TRANSACTION_DATE",
        "Post Date": "POST_DATE",
        "Description": "DESCRIPTION",
        "Category": "CATEGORY",
        "Type": "TRANSACTION_TYPE",
        "Amount": "CHASE_CREDIT_CARD_AMOUNT",
        "Memo": "DROP"
    }

    chase_bank_map = {
        "Details": "DETAILS",  # must lowercase it
        "Posting Date": "POST_DATE",
        "Description": "DESCRIPTION",
        "Amount": "BANK_AMOUNT",  # must take the absolute value
        "Type": "TYPE_DETAIL",  # authority
        "Balance": "DROP",
        "Check or Slip #": "check_number"
    }