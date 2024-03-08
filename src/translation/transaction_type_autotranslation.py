class TransactionTypeAutotranslation:
    # from: to
    trans_type_autotranslation = {
        "adjustment": "adjustment",
        "check": "debit",
        "fee": "debit",
        "payment": "credit_card_payment",
        "payment/credit": "credit_card_payment",
        "purchase": "debit",
        "return": "credit",
        "sale": "debit"
    }

