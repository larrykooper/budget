class TransactionTypeAutotranslation:
    # from: to
    trans_type_autotranslation = {
        "adjustment": "adjustment",
        "check": "debit",
        "fee": "debit",
        "payment": "credit_card_payment",
        "payment/credit": "transfer",
        "purchase": "debit",
        "return": "credit",
        "sale": "debit"
    }

