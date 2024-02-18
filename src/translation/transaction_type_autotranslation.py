class TransactionTypeAutotranslation:
    # from: to
    trans_type_autotranslation = {
        "Adjustment": "adjustment",
        "Fee": "debit",
        "Payment": "transfer",
        "Payment/Credit": "transfer",
        "Purchase": "debit",
        "Return": "credit",
        "Sale": "debit"
    }

    bank_trans_detail_to_trans_type = {
        "ACH_CREDIT": "credit",
        "ACH_DEBIT": "debit",
        "ATM": "debit",
        "CHECK_PAID": "debit",
        "DEBIT_CARD": "debit",
        "FEE_TRANSACTION": "debit",
        "LOAN_PMT": "transfer",
        "MISC_DEBIT": "debit"
    }