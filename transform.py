import pandas as pd

df = pd.read_csv("ventas_sucias.csv")
#Eliminar los duplicados
df = df.drop_duplicates(subset="id_venta")

#Estandarizar los textos que existen, eliminando espacios y dejando todo en mayusculas
df["cliente"] = df["cliente"].str.strip().str.title()
df["producto"] = df["producto"].str.strip().str.title()

#Probar tres formatos distintos de fecha
def parsear_fecha(texto):
    for formato in ("%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"):
        try:
            return pd.to_datetime(texto, format=formato)
        except ValueError:
            continue
    return pd.NaT

df["fecha"] = df["fecha"].apply(parsear_fecha)

# A los precios nulos le asignamos un precio común por producto
precio_por_producto = df.groupby("producto")["precio_unitario"].transform("max")
df["precio_unitario"] = df["precio_unitario"].fillna(precio_por_producto)

# Columna calculada
df["total"] = df["cantidad"] * df["precio_unitario"]

# Chequeo final para verificar los cambios
print("Filas finales:", len(df))
print("Fechas inválidas:", df["fecha"].isna().sum())
print("Precios nulos:", df["precio_unitario"].isna().sum())
print("Clientes:", df["cliente"].unique())
print(df.dtypes)
print(df.head())

df.to_csv("ventas_limpias.csv", index=False)
