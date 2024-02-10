import csv
from decimal import Decimal

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder
from src.models.line_item import LineItem
from src.translation.category_setter import CategorySetter
from src.translation.column_map import ColumnMap
from src.translation.transaction_type_setter import TransactionTypeSetter
from src.translation.translator import Translator

def ingest_file(filename: str, account: str):
    from src.flask_app.ingesting.upload_file import UPLOAD_FOLDER

    # Intialize the repo

    repo = LarryRepository()
    authority_finder = AuthorityFinder()

    # Look up account ID
    account_id = authority_finder.authority_lookup("account", account)
    """
    TEMP COMMENT
    account_id is 1
    """


    # App-specific initialization

    translator = Translator()
    category_setter = CategorySetter()
    trans_type_setter = TransactionTypeSetter()

    # Reading the file

    filepath = f"{UPLOAD_FOLDER}/{filename}"

    # filepath = '/Users/larry1mbp/mycode/python/budget/sample_data/Chase3307_small.CSV'

    with open(filepath, mode='r') as f:
        csv_reader = csv.DictReader(f)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                translator.process_first_line()
            line_item_dict = {"account_id": account_id}
            # Iterate thru the fields in this line
            for csv_key, value in row.items():
                db_key = ColumnMap.chase_cc_map[csv_key]
                match db_key:
                    case "CATEGORY":
                        cat = category_setter.get_category(value, row["Description"])
                        line_item_dict["category_id"] = cat
                    case "TRANSACTION_TYPE":
                        trans_type_id = trans_type_setter.get_trans_type(value)
                        line_item_dict["transaction_type_id"] = trans_type_id
                    case "AMOUNT":
                        amount_d = Decimal(value)
                        line_item_dict['amount'] = -1 * amount_d
                    case "DROP":
                        pass
                    case _:
                        line_item_dict[db_key] = value

            line_item = LineItem(**line_item_dict)
            line_count += 1
            repo.add(line_item)

    # for each line:
    # translate some columns into authorities
    #   Category and Type need to be changed to authorities
    #   later - autocategorize based on payee
    # Write 1 row to the line_item table
