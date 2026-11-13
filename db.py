import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()  

def get_engine(**kwargs):
    password = os.getenv("MSSQL_SA_PASSWORD")
    if not password:
        raise RuntimeError("Falta MSSQL_SA_PASSWORD en el archivo .env")

    url = URL.create(
        "mssql+pyodbc",
        username="sa",
        password=password,
        host="localhost",
        port=1433,
        database="mini_etl",
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "TrustServerCertificate": "yes",
        },
    )
    return create_engine(url, **kwargs)
