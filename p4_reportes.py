import pandas as pd
import numpy as np

try:
    df_final = pd.read_csv('df_integrado_p1.csv')
except FileNotFoundError:
    print("Error: No se encontró el archivo df_integrado_p1.csv. Asegúrate de ejecutar p1_integracion.py primero.")
    exit()

df_final['Cliente'] = df_final['Cliente'].astype(str)
df_final['Producto'] = df_final['Producto'].astype(str)
df_final['Ciudad'] = df_final['Ciudad'].astype(str)
df_final['Categoria_Cliente'] = df_final['Categoria_Cliente'].astype(str)

df_final.dropna(subset=['Cliente', 'Producto', 'Ciudad', 'Categoria_Cliente'], inplace=True)

agrupaciones = ['Cliente', 'Producto', 'Ciudad', 'Categoria_Cliente']

metricas = {
    'Total': 'sum',
    'PrecioUnitario': 'mean',
    'Cantidad': 'count'
}

df_reporte = df_final.groupby(agrupaciones).agg(metricas).reset_index()

df_reporte.rename(columns={
    'Total': 'Suma_Total',
    'PrecioUnitario': 'Promedio_PrecioUnitario',
    'Cantidad': 'Cantidad_Compras'
}, inplace=True)


df_reporte.sort_values(by=['Ciudad', 'Suma_Total'], ascending=[True, False], inplace=True)

df_reporte.to_csv('reporte_multinivel.csv', index=False)
print("--- PROBLEMA 4: Agrupaciones y Reportes Multinivel ---")
print("¡Exportación exitosa! Archivo 'reporte_multinivel.csv' generado.")

df_volumen_ciudad = df_reporte.groupby('Ciudad')['Suma_Total'].sum().sort_values(ascending=False)
ciudad_mayor_volumen = df_volumen_ciudad.index[0]
total_ciudad = df_volumen_ciudad.iloc[0]

df_variedad_cliente = df_reporte.groupby('Cliente')['Producto'].nunique().sort_values(ascending=False)
cliente_mayor_variedad = df_variedad_cliente.index[0]
conteo_variedad = df_variedad_cliente.iloc[0]

print(f"\nLa ciudad con mayor volumen total es: {ciudad_mayor_volumen} (Total: ${total_ciudad:,.2f})")
print(f"El cliente con mayor variedad de productos es: {cliente_mayor_variedad} ({conteo_variedad} productos distintos)")

print("\nPrimeras 10 filas del reporte multinivel ordenado:")
print(df_reporte.head(10).to_string(index=False))
