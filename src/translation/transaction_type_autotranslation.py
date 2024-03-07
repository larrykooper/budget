class TransactionTypeAutotranslation:
    # from: to
    trans_type_autotranslation = {
        "Adjustment": "adjustment",
        "check": "debit",
        "Fee": "debit",
        "Payment": "transfer",
        "Payment/Credit": "transfer",
        "Purchase": "debit",
        "Return": "credit",
        "Sale": "debit"
    }

