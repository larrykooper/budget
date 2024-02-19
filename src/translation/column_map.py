class ColumnMap:

#  map from: map to
# If capital letters, it has some special processing. If not, it is just copied

    chase_cc_map = {
        "Transaction Date": "transaction_date",
        "Post Date": "post_date",
        "Description": "description",
        "Category": "CATEGORY",
        "Type": "TRANSACTION_TYPE",
        "Amount": "AMOUNT",
        "Memo": "DROP"
    }

    chase_bank_map = {
        "Details": "DETAILS"  # must lowercase it
        "Posting Date": "post_date"
        "Description": "description",
        "Amount": "BANK_AMOUNT"  # must take the absolute value
        "Type": "TYPE_DETAIL"  # authority
        "Balance": "DROP",
        "Check or Slip #": "check_number"
    }