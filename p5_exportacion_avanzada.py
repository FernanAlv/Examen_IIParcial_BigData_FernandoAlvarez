import pandas as pd
import os

ventas = pd.read_csv('ventas.csv')
clientes = pd.read_csv('clientes.csv')
productos = pd.read_csv('productos.csv')

productos_validos = productos['Producto'].dropna().astype(str).str.strip().unique()
clientes_validos = clientes['Cliente'].dropna().astype(str).str.strip().unique()

ventas_limpias = ventas.copy()
ventas_limpias['Producto'] = ventas_limpias['Producto'].astype(str).str.strip()
ventas_limpias = ventas_limpias[ventas_limpias['Producto'].isin(productos_validos)]
ventas_limpias['Cliente'] = ventas_limpias['Cliente'].astype(str).str.strip()
ventas_limpias = ventas_limpias[ventas_limpias['Cliente'].isin(clientes_validos)]

for col in ['Cantidad', 'PrecioUnitario', 'Total']:
    ventas_limpias[col] = pd.to_numeric(ventas_limpias[col], errors='coerce')
    promedio = ventas_limpias[col].mean()
    ventas_limpias[col] = ventas_limpias[col].fillna(promedio)

os.makedirs('salidas', exist_ok=True)

resumen_global = []

for producto in ventas_limpias['Producto'].unique():
    prod_limpio = str(producto).strip().replace('/', '_').replace('\\', '_')
    carpeta = f'salidas/Producto={prod_limpio}'
    os.makedirs(carpeta, exist_ok=True)
    
    df_prod = ventas_limpias[ventas_limpias['Producto'] == producto]
    archivo = f'{carpeta}/archivo.csv'
    df_prod.to_csv(archivo, index=False)
    
    total_ventas = df_prod['Total'].sum()
    cant_registros = len(df_prod)
    precio_prom = df_prod['PrecioUnitario'].mean()
    
    with open(f'{carpeta}/resumen.txt', 'w') as f:
        f.write(f"Total de ventas del producto: {total_ventas:.2f}\n")
        f.write(f"Cantidad de registros: {cant_registros}\n")
        f.write(f"Precio Unitario promedio: {precio_prom:.2f}\n")
    
    resumen_global.append({
        'Producto': producto,
        'Total_Ventas': total_ventas,
        'Cantidad_Registros': cant_registros,
        'Precio_Promedio': precio_prom
    })

pd.DataFrame(resumen_global).to_csv('resumen_global.csv', index=False)
print("Exportación completada. Revisa la carpeta 'salidas/' y archivos resumen.")
