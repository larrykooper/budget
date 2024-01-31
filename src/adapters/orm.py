from sqlalchemy import (
    Column,
    Date,
    ForeignKey,   
    Integer,
    MetaData,  
    Numeric,
    String,
    Table,   
)
from sqlalchemy.orm import registry 

from src.models.line_item import LineItem 

metadata = MetaData()
mapper_registry = registry()

line_item = Table(
    "line_item",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("transaction_date", Date),
    Column("post_date", Date),
    Column("description", String(255)),
    Column("amount", Numeric(8,2)),
    Column("category_id", ForeignKey("category.id")),
    Column("transaction_type_id", ForeignKey("transaction_type.id")),
    Column("account_id", ForeignKey("account.id")),
    Column("check_number", String(10)),
    Column("type_detail_id", ForeignKey("type_detail.id"), nullable=True),     # optional     
)

account = Table(
    "account",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255))
)

category = Table(
    "category",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255))
)

type_detail = Table(
    "type_detail",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255))
)

account = Table(
    "transaction_type",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255))
)

"""
To use the classical mapping (aka the Imperative mapping)
we define an explicit mapper for how to convert between 
the schema and our domain model. 
https://docs.sqlalchemy.org/en/20/orm/mapping_styles.html
"""
def start_mappers():
    mapper_registry.map_imperatively(LineItem, line_item)
    