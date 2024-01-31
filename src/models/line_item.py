from datetime import date
from decimal import * 
from typing import Optional 

class LineItem:
    def __init__(
        self, 
        transaction_date: date,
        post_date: date,
        description: str,
        amount: Decimal, 
        category_id: int,
        transaction_type_id: int,
        account_id: int,
        check_number: str,
        type_detail_id: Optional[int]
    ):
        self.transaction_date = transaction_date
        self.post_date = post_date
        self.description = description
        self.amount = amount
        self.category_id = category_id
        self.transaction_type_id = transaction_type_id
        self.account_id = account_id
        self.check_number = check_number
        self.type_detail_id = type_detail_id
