from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.sql_alchemy_repository import SqlAlchemyRepository

import src.setup.config as config 
import src.adapters.orm as orm 

# Start things up - initialize the app and the repo 

orm.start_mappers()
get_session = sessionmaker(bind=create_engine(config.get_postgres_uri()))
session = get_session()
repo = SqlAlchemyRepository(session)

#  version 0 - file path is hard coded 
#  version 1 - user puts the file path on command line
#  version 2 - User can browse in a dialog box for the file name 

# Read in entire file 

filepath = '/Users/larry1mbp/mycode/python/budget/sample_data/Chase3307_small.CSV'

with open(filepath) as f:
    input_lines = f.readlines()

repo = SqlAlchemyRepository(session)

for line in input_lines:
    # Do some things, to create the line_item 
    print("I am adding a line item")
    #repo.add(line_item)

    

# for each line: 
  # translate some columns into authorities 
  #   Category and Type need to be changed to authorities 
  #   later - autocategorize based on payee 
  # Write 1 row to the line_item table 




