from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
from db import get_engine

url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="@Pokemon100",   # aquí puede llevar @, !, etc.
    host="localhost",
    port=1433,
    database="mini_etl",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)

engine = get_engine()

with engine.connect() as conn:
    print(conn.execute(text("SELECT name FROM sys.schemas WHERE name IN ('staging','dw')")).fetchall())
