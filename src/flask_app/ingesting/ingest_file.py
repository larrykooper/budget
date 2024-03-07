import csv

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

    # Read the file

    filepath = f"{UPLOAD_FOLDER}/{filename}"

    with open(filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                continue
            # Add the account_id to the line item
            line_item_dict = {"account_id": account_id}
            # Iterate thru the fields in the line
            for csv_key, value in row.items():
                field_type_str = column_map[csv_key]
                kwargs = {}
                if field_type_str == "DROP":
                    continue
                if field_type_str == "CATEGORY":
                    kwargs = {'description': row["Description"]}
                field_type_obj = InputField.instantiate_input_field(field_type_str)
                what_to_persist = field_type_obj.what_to_persist(value, **kwargs)
                line_item_field_name = field_type_obj.line_item_field_name()
                line_item_dict[line_item_field_name] = what_to_persist
            line_item = LineItem(**line_item_dict)
            line_count += 1
            repo.add(line_item)

    # for each line:
    # translate some columns into authorities
    #   Category and Type need to be changed to authorities
    #   later - autocategorize based on payee
    # Write 1 row to the line_item table
