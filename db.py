from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Text, TIMESTAMP, JSON
from sqlalchemy.sql import func

engine = create_engine(
    "postgresql+psycopg2://hackathon:hackathon123@localhost:5432/legacy_db"
)

metadata = MetaData()

# Table for tabular data (one row per record)
legacy_tabular = Table(
    "legacy_tabular",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", Text),
    Column("upload_time", TIMESTAMP, server_default=func.now()),
    Column("row_data", JSON),
)

# Table for non-tabular commands (JSON array)
legacy_commands = Table(
    "legacy_commands",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("filename", Text),
    Column("upload_time", TIMESTAMP, server_default=func.now()),
    Column("commands", JSON),
)

metadata.create_all(engine)
