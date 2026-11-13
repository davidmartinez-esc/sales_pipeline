import pandas as pd

df = pd.read_csv("ventas_sucias.csv")

print(df.head(10))
print(df.info())
print("Nulos por columna:\n", df.isna().sum())
print("Duplicados:", df.duplicated().sum())
print("Clientes distintos:", df["cliente"].unique())
