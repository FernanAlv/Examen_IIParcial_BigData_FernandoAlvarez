import pandas as pd
import os

total_final = 0
ventas_por_producto = {}
mejor_chunk = {'total': 0, 'num': 0}

for i, chunk in enumerate(pd.read_csv('ventas.csv', chunksize=1000)):
    chunk['Cantidad'] = pd.to_numeric(chunk['Cantidad'], errors='coerce').fillna(0)
    chunk['PrecioUnitario'] = pd.to_numeric(chunk['PrecioUnitario'], errors='coerce').fillna(0)
    chunk['Total'] = pd.to_numeric(chunk['Total'], errors='coerce').fillna(0)
    
    chunk['Subtotal'] = chunk['Cantidad'] * chunk['PrecioUnitario']
    
    def calcular_impuesto(total):
        if total < 5000:
            return total * 0.10
        elif total <= 20000:
            return total * 0.15
        else:
            return total * 0.18
    
    chunk['Impuesto'] = chunk['Total'].apply(calcular_impuesto)
    chunk_total = chunk['Total'].sum()
    total_final += chunk_total
    
    chunk['Producto'] = chunk['Producto'].astype(str).str.strip()
    for producto in chunk['Producto']:
        ventas_por_producto[producto] = ventas_por_producto.get(producto, 0) + chunk['Cantidad'].sum()
    
    if chunk_total > mejor_chunk['total']:
        mejor_chunk = {'total': chunk_total, 'num': i+1}

print(f"Total Final Global: {total_final:.2f}")
print("Top 5 productos más vendidos:")
top_productos = sorted(ventas_por_producto.items(), key=lambda x: x[1], reverse=True)[:5]
for prod, ventas in top_productos:
    print(f"- {prod}: {ventas}")
print(f"El chunk con mayor contribución: Chunk {mejor_chunk['num']} (${mejor_chunk['total']:.2f})")
