import csv
import hashlib

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder
from src.models.account_types.account import Account
from src.models.input_field_types.input_field import InputField
from src.models.line_item import LineItem
from src.translation.category_rules import CategoryRules


def ingest_file(filename: str, account: str):
    from src.flask_app.ingesting.upload_file import UPLOAD_FOLDER

    # Intialize the repo

    repo = LarryRepository()
    authority_finder = AuthorityFinder()

    # Look up account ID
    account_id = authority_finder.authority_lookup("account", account)
    account_obj = Account.instantiate_account(account)
    column_map = account_obj.column_map()

    # Module-specific initialization

    CategoryRules.initialize_category_rules()
    rejected_inserts = []

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
            line_item = LineItem(**line_item_dict)
            line_count += 1
            data_hash = hash_the_data(line_item)
            if hash_exists(repo, data_hash):
                rejected_inserts.append(line_item)
            else:
                line_item.data_hash = data_hash
                repo.add(line_item)
    if rejected_inserts:
        return "INSERTS REJECTED", rejected_inserts
    else:
        return "SUCCESS"

def hash_the_data(line_item: LineItem) -> str:
        transaction_date = line_item.transaction_date
        amount = line_item.amount
        description = line_item.description
        to_hash = f"{transaction_date}|{amount}|{description}"
        as_bytes = to_hash.encode(encoding='utf-8', errors='strict')
        return hashlib.sha256(as_bytes).hexdigest()

def hash_exists(repo: LarryRepository, hash: str) -> bool:
    result = repo.query_for_hash(hash)
    if result is None:
        return False
    else:
        return True

