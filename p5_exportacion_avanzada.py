import pandas as pd
import numpy as np
import os
import re

def clean_name(name):

    cleaned = str(name).strip()
    cleaned = re.sub(r'[^\w\s-]', '', cleaned)
    cleaned = re.sub(r'\s+', '_', cleaned)
    return cleaned

df_ventas = pd.read_csv("ventas.csv")
df_clientes = pd.read_csv("Clientes.csv").reset_index().iloc[:, :3]
df_clientes.columns = ['Cliente', 'Ciudad', 'Categoria_Cliente']
df_clientes = df_clientes.dropna(subset=['Cliente'], how='all').astype(str)
df_productos = pd.read_csv("productos.csv").reset_index().iloc[:, :3]
df_productos.columns = ['Producto', 'Categoria_Producto', 'Impuesto']
df_productos = df_productos.dropna(subset=['Producto'], how='all').astype(str)

columnas_numericas = ['Cantidad', 'PrecioUnitario', 'Total']
for col in columnas_numericas:
    df_ventas[col] = pd.to_numeric(df_ventas[col], errors='coerce')
    promedio = df_ventas[col].mean()
    df_ventas[col].fillna(promedio, inplace=True)

producto_mapping = {
    'Mouse inalámbrico': 'Mouse', 'Audífonos Bluetooth': 'Audífonos', 
    'Teclado mecánico': 'Teclado', 'Monitor 24"': 'Monitor',
}
df_ventas['Producto_Mapeado'] = df_ventas['Producto'].apply(lambda x: producto_mapping.get(x, x))
clientes_ventas_unique = df_ventas['Cliente'].unique()
clientes_catalogo_unique = df_clientes['Cliente'].unique()
if len(clientes_ventas_unique) > 0:
    client_map = dict(zip(clientes_ventas_unique, clientes_catalogo_unique[:len(clientes_ventas_unique)]))
    df_ventas['Cliente'] = df_ventas['Cliente'].map(client_map)
df_ventas = df_ventas[df_ventas['Producto_Mapeado'].isin(df_productos['Producto'].unique())].copy()
df_ventas['Producto'] = df_ventas['Producto_Mapeado']
df_ventas.drop(columns=['Producto_Mapeado'], inplace=True)
df_ventas = df_ventas[df_ventas['Cliente'].isin(df_clientes['Cliente'].unique())].copy()

df_final = pd.merge(df_ventas, df_clientes, on='Cliente', how='left')
df_final = pd.merge(df_final, df_productos[['Producto', 'Categoria_Producto', 'Impuesto']], on='Producto', how='left')

output_base_dir = "salidas"
os.makedirs(output_base_dir, exist_ok=True)
resumen_global_data = []


for producto, df_group in df_final.groupby('Producto'):
    
    producto_limpio = clean_name(producto)
    output_dir = os.path.join(output_base_dir, f"Producto={producto_limpio}")
    os.makedirs(output_dir, exist_ok=True)
    
    total_ventas = df_group['Total'].sum()
    cantidad_registros = len(df_group)
    precio_unitario_promedio = df_group['PrecioUnitario'].mean()

    resumen_path = os.path.join(output_dir, "resumen.txt")
    with open(resumen_path, 'w') as f:
        f.write(f"Producto: {producto}\n")
        f.write(f"Total de ventas del producto: {total_ventas:,.2f}\n")
        f.write(f"Cantidad de registros: {cantidad_registros}\n")
        f.write(f"Precio Unitario promedio: {precio_unitario_promedio:,.2f}\n")

    archivo_path = os.path.join(output_dir, "archivo.csv")
    df_group.to_csv(archivo_path, index=False)
    
    resumen_global_data.append({
        'Producto': producto,
        'Total_Ventas': total_ventas,
        'Cantidad_Registros': cantidad_registros,
        'Precio_Unitario_Promedio': precio_unitario_promedio
    })

df_resumen_global = pd.DataFrame(resumen_global_data)
df_resumen_global.to_csv(os.path.join(output_base_dir, "resumen_global.csv"), index=False)

print("\n--- Exportación Segmentada Finalizada ---")
print(f"El resumen global fue exportado a './salidas/resumen_global.csv' ({len(df_resumen_global)} productos).")
