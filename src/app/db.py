import os

from databases import Database
from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    String,
    Table,
    create_engine,
    MetaData
)
from sqlalchemy.sql import func

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")

database_url = f"postgresql://{DB_USER}:{DB_PASS}@db/{DB_NAME}"

engine = create_engine(database_url)
metadata = MetaData()
notes = Table(
    "notes",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("title", String(50)),
    Column("description", String(50)),
    Column("created_date", DateTime, default=func.now(), nullable=False)
)

database = Database(database_url)
