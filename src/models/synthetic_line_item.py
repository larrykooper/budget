# A SyntheticLineItem is a transaction added when we get a medical reimbursement
# It's meant to offset spending on Doctor
# The table is used to avoid creating duplicate synthetic transactions

class SyntheticLineItem:

    def __init__(
        self,
        line_item_id: int,   # FK to the line_item
        deposit_based_on: int # line_item_id of the deposit the synth item is based on
    ):
        self.line_item_id = line_item_id
        self.deposit_based_on = deposit_based_on
