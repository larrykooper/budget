import datetime
from datetime import date
from decimal import Decimal
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
        check_number: Optional[str] = None,
        type_detail_id: Optional[int] = None,
        comment: str = None,
        data_hash: str = None,
        created: datetime.datetime = None,
        updated: datetime.datetime = None,
        show_on_spending_report: bool = True,
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
        self.comment = comment
        self.data_hash = data_hash
        self.created = created
        self.updated = updated
        self.show_on_spending_report =  show_on_spending_report



