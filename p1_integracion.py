import pandas as pd
import numpy as np

total_inicial = 0
filas_rechazadas = 0

df_ventas = pd.read_csv("ventas.csv")

df_clientes = pd.read_csv("Clientes.csv")
df_clientes = df_clientes.reset_index().iloc[:, :3]
df_clientes.columns = ['Cliente', 'Ciudad', 'Categoria_Cliente']
df_clientes = df_clientes.dropna(subset=['Cliente', 'Ciudad', 'Categoria_Cliente'], how='all').astype(str)

df_productos = pd.read_csv("productos.csv")
df_productos = df_productos.reset_index().iloc[:, :3]
df_productos.columns = ['Producto', 'Categoria_Producto', 'Impuesto']
df_productos = df_productos.dropna(subset=['Producto', 'Categoria_Producto', 'Impuesto'], how='all').astype(str)

total_inicial = len(df_ventas)

producto_mapping = {
    'Mouse inalámbrico': 'Mouse',
    'Audífonos Bluetooth': 'Audífonos',
    'Teclado mecánico': 'Teclado',
    'Monitor 24"': 'Monitor',
}

df_ventas['Producto_Mapeado'] = df_ventas['Producto'].apply(lambda x: producto_mapping.get(x, x))


clientes_ventas_unique = df_ventas['Cliente'].unique()
clientes_catalogo_unique = df_clientes['Cliente'].unique()
if len(clientes_ventas_unique) > 0:
    client_map = dict(zip(clientes_ventas_unique, clientes_catalogo_unique[:len(clientes_ventas_unique)]))
    df_ventas['Cliente'] = df_ventas['Cliente'].map(client_map)

productos_validos = df_productos['Producto'].unique()
ventas_antes_prod_filter = len(df_ventas)

df_ventas = df_ventas[df_ventas['Producto_Mapeado'].isin(productos_validos)].copy()
filas_rechazadas += (ventas_antes_prod_filter - len(df_ventas))

df_ventas['Producto'] = df_ventas['Producto_Mapeado']
df_ventas.drop(columns=['Producto_Mapeado'], inplace=True)


clientes_validos = df_clientes['Cliente'].unique()
ventas_antes_cliente_filter = len(df_ventas)

df_ventas = df_ventas[df_ventas['Cliente'].isin(clientes_validos)].copy()
filas_rechazadas += (ventas_antes_cliente_filter - len(df_ventas))

columnas_numericas = ['Cantidad', 'PrecioUnitario', 'Total']

for col in columnas_numericas:
    
    df_ventas[col] = pd.to_numeric(df_ventas[col], errors='coerce')

    promedio = df_ventas[col].mean()

    df_ventas[col].fillna(promedio, inplace=True)

df_final = pd.merge(df_ventas, df_clientes, on='Cliente', how='left')

df_final = pd.merge(df_final, df_productos[['Producto', 'Categoria_Producto', 'Impuesto']], on='Producto', how='left')


filas_finales = len(df_final)

print(f"Total de filas iniciales: {total_inicial}")
print(f"Filas rechazadas (por Producto o Cliente no existente): {filas_rechazadas}")
print(f"Filas finales en el DataFrame integrado: {filas_finales}")

print("\nPrimeras 10 filas del DataFrame final:")
print(df_final.head(10).to_string(index=False))

df_final.to_csv("df_integrado_p1.csv", index=False)
