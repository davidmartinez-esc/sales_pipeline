import pandas as pd
import random
from datetime import date, timedelta

random.seed(42)

clientes = ["ana perez", "LUIS GOMEZ", "  maria soto", "Pedro Rojas", "carla DIAZ", "Jorge Vega "]
productos = {"Laptop": 550000, "Mouse": 12000, "Teclado": 25000, "Monitor": 140000, "Audifonos": 30000}
formatos = ["%Y-%m-%d", "%d/%m/%Y", "%d-%m-%Y"]

filas = []
for i in range(1, 201):
    producto = random.choice(list(productos))
    fecha = date(2026, 1, 1) + timedelta(days=random.randint(0, 300))
    precio = productos[producto] if random.random() > 0.05 else None
    filas.append({
        "id_venta": i,
        "fecha": fecha.strftime(random.choice(formatos)),
        "cliente": random.choice(clientes),
        "producto": producto,
        "cantidad": random.randint(1, 5),
        "precio_unitario": precio,
    })

df = pd.DataFrame(filas)
duplicados = df.sample(10, random_state=1)
df = pd.concat([df, duplicados]).sample(frac=1, random_state=2)

df.to_csv("ventas_sucias.csv", index=False)
print("CSV generado:", len(df), "filas")
