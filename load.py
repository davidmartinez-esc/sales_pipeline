import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import URL
from db import get_engine

DDL = """
IF OBJECT_ID('dw.fact_ventas') IS NOT NULL DROP TABLE dw.fact_ventas;
IF OBJECT_ID('dw.dim_cliente') IS NOT NULL DROP TABLE dw.dim_cliente;
IF OBJECT_ID('dw.dim_producto') IS NOT NULL DROP TABLE dw.dim_producto;

CREATE TABLE dw.dim_cliente (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nombre     VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE dw.dim_producto (
    id_producto INT IDENTITY(1,1) PRIMARY KEY,
    nombre      VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE dw.fact_ventas (
    id_venta        INT PRIMARY KEY,
    fecha           DATE NOT NULL,
    id_cliente      INT NOT NULL REFERENCES dw.dim_cliente(id_cliente),
    id_producto     INT NOT NULL REFERENCES dw.dim_producto(id_producto),
    cantidad        INT NOT NULL,
    precio_unitario DECIMAL(12,2) NOT NULL,
    total           DECIMAL(14,2) NOT NULL
);
"""

url = URL.create(
    "mssql+pyodbc",
    username="sa",
    password="@Pokemon100",
    host="localhost",
    port=1433,
    database="mini_etl",
    query={
        "driver": "ODBC Driver 18 for SQL Server",
        "TrustServerCertificate": "yes",
    },
)

engine = get_engine()

raw = pd.read_csv("ventas_sucias.csv")
limpio = pd.read_csv("ventas_limpias.csv", parse_dates=["fecha"])


with engine.connect() as conn:       
    # Guardamos datos en crudo
    raw.to_sql("ventas_raw", conn, schema="staging", if_exists="replace", index=False)

    # Borrar y volver a crear las tablas del data warehouse
    conn.execute(text(DDL))

    # Hacemos las tablas las cuales tienen valores unicos como producto o el nombre del cliente
    # Esto lo hacemos para no guardar strings y strings de nombre cliente todas las veces que
    # un cliente realiza una compra
    (limpio[["cliente"]].drop_duplicates()
        .rename(columns={"cliente": "nombre"})
        .to_sql("dim_cliente", conn, schema="dw", if_exists="append", index=False))

    (limpio[["producto"]].drop_duplicates()
        .rename(columns={"producto": "nombre"})
        .to_sql("dim_producto", conn, schema="dw", if_exists="append", index=False))

    # Leer las dimensiones para obtener los IDs que generó SQL Server
    dim_cli = pd.read_sql("SELECT id_cliente, nombre AS cliente FROM dw.dim_cliente", conn)
    dim_prod = pd.read_sql("SELECT id_producto, nombre AS producto FROM dw.dim_producto", conn)

    # Tabla de ventas realizadas, reemplazamos el nombre de las personas por las IDs de ellas
    fact = (limpio
            .merge(dim_cli, on="cliente")
            .merge(dim_prod, on="producto")
            [["id_venta", "fecha", "id_cliente", "id_producto",
              "cantidad", "precio_unitario", "total"]])
    fact.to_sql("fact_ventas", conn, schema="dw", if_exists="append", index=False)

print("Staging:", len(raw), "filas | Hechos:", len(fact), "filas")
