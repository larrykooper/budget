import csv
import hashlib

from src.adapters.repositories.authority_repository import AuthorityRepository
from src.adapters.repositories.line_item.line_item_write import LineItemWrite
from src.models.account_types.account import Account
from src.models.input_field_types.input_field import InputField
from src.models.line_item import LineItem

def ingest_file(filename: str, account: str):
    from src.flask_app.ingesting.upload_file import UPLOAD_FOLDER

    # Intialize the repo

    line_item_write = LineItemWrite()
    authority_repo = AuthorityRepository()

    # Look up account ID
    account_id = authority_repo.authority_lookup("account", account)
    account_obj = Account.instantiate_account(account)
    column_map = account_obj.column_map()

    # Module-specific initialization

    default_trans_id = get_default_trans_id()

    # Read the file

    filepath = f"{UPLOAD_FOLDER}/{filename}"

    with open(filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        for row in csv_reader:
            # Add the account_id to the line item
            line_item_dict = {"account_id": account_id}
            # Iterate thru the fields in the line
            for csv_key, value in row.items():
                if not csv_key:
                    continue
                field_type_str = column_map[csv_key]
                kwargs = {}
                if field_type_str == "DROP":
                    continue
                if field_type_str == "CATEGORY":
                    kwargs = {'description': row["Description"]}
                field_type_obj = InputField.instantiate_input_field(field_type_str)
                what_to_persist = field_type_obj.what_to_persist(value, **kwargs)
                for field_name, persist_value in what_to_persist.items():
                    line_item_dict[field_name] = persist_value
            if not "transaction_type_id" in line_item_dict:
                line_item_dict["transaction_type_id"] = default_trans_id
            line_item = LineItem(**line_item_dict)
            line_count += 1
            data_hash = hash_the_data(line_item)
            line_item.data_hash = data_hash
            line_item_write.add_line_item(line_item)
        # Done with ingesting the whole file
        # Set items NOT to show on spending report if necessary
        line_item_write.update_show_on_spending_report()
        return "SUCCESS"

def hash_the_data(line_item: LineItem) -> str:
        transaction_date = line_item.transaction_date
        amount = line_item.amount
        description = line_item.description
        to_hash = f"{transaction_date}|{amount}|{description}"
        as_bytes = to_hash.encode(encoding='utf-8', errors='strict')
        return hashlib.sha256(as_bytes).hexdigest()

def get_default_trans_id() -> int:
    authority_repo = AuthorityRepository()
    default_type = "debit"
    return authority_repo.authority_lookup("transaction_type", default_type)

