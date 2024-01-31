import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.larry_repository import LarryRepository
from src.authorities.authority_finder import AuthorityFinder
from src.models.line_item import LineItem
from src.translation.column_map import ColumnMap
from src.translation.translator import Translator

# Start things up - initialize the repo 


repo = LarryRepository()
authority_finder = AuthorityFinder()

#  version 0 - file path is hard coded 
#  version 1 - user puts the file path on command line
#  version 2 - User can browse in a dialog box for the file name 

"""
I have to tell the program which account the file being uploaded is for.
Version 0 - I will hard-code the account
""" 

account = "Amazon-3307"
account_id = authority_finder.authority_lookup("account", account)

# App-specific initialization 

translator = Translator()

# Reading file stuff

filepath = '/Users/larry1mbp/mycode/python/budget/sample_data/Chase3307_small.CSV'

with open(filepath, mode='r') as f:
    csv_reader = csv.DictReader(f)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            translator.process_first_line()
        line_item_dict = {"account_id": account_id}    
        # Iterate thru the fields in this line
        #  Refactor this later? 
        for csv_key, value in row.items():
            db_key = ColumnMap.chase_cc_map[csv_key]
            match db_key:
                case "AUTHORITY":
                    print("looking up authority now")
                case "DROP":
                    pass
                case _:            
                    line_item_dict[db_key] = value
          
        line_item = LineItem(**line_item_dict)       
        line_count += 1   
        print("I am adding a line item")
        repo.add(line_item)

    

# for each line: 
  # translate some columns into authorities 
  #   Category and Type need to be changed to authorities 
  #   later - autocategorize based on payee 
  # Write 1 row to the line_item table 
    





