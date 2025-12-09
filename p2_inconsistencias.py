import pandas as pd

ventas = pd.read_csv('ventas.csv')
clientes = pd.read_csv('clientes.csv')
productos = pd.read_csv('productos.csv')

ventas.columns = [c.strip() for c in ventas.columns]
clientes.columns = [c.strip() for c in clientes.columns]
productos.columns = [c.strip() for c in productos.columns]

map_cols = {
    'cantidad': 'Cantidad',
    'preciounitario': 'PrecioUnitario',
    'total': 'Total',
    'producto': 'Producto',
    'cliente': 'Cliente'
}

cols_lower = {c.lower(): c for c in ventas.columns}
for k, v in map_cols.items():
    if v not in ventas.columns and k in cols_lower:
        ventas.rename(columns={cols_lower[k]: v}, inplace=True)

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

ventas_limpias['Subtotal'] = ventas_limpias['Cantidad'] * ventas_limpias['PrecioUnitario']
ventas_limpias['Diferencia'] = (ventas_limpias['Subtotal'] - ventas_limpias['Total']).abs()
ventas_limpias['Error_Relativo'] = ventas_limpias['Diferencia'] / ventas_limpias['Total'] * 100

inconsistencias = ventas_limpias[ventas_limpias['Error_Relativo'] > 5]
inconsistencias.to_csv('inconsistencias.csv', index=False)

print(f"Total de registros inconsistentes: {len(inconsistencias)}")
if len(inconsistencias) > 0:
    print(f"Promedio del error relativo: {inconsistencias['Error_Relativo'].mean():.2f}%")
    producto_mas_inconsistente = inconsistencias['Producto'].value_counts().index[0]
    print(f"Producto con más inconsistencias: {producto_mas_inconsistente}")
else:
    print("Promedio del error relativo: 0.00%")
    print("Producto con más inconsistencias: N/A")
