import pandas as pd


df_tienda = pd.read_csv("moda_limpio.csv")

print(">>> ANÁLISIS VISUAL DE LA TIENDA <<<")

producto_top = df_tienda['categoria'].value_counts().idxmax()
cantidad_top = df_tienda['categoria'].value_counts().max()

print(f"1. Categoría más frecuente: {producto_top}")
print(f" Cantidad de ventas: {cantidad_top}")

promedio_precios = df_tienda['ventas'].mean()
print(f"2. Promedio general de ventas: ${promedio_precios:.2f}")

total_productos = df_tienda['categoria'].nunique()
print(f"3. Total de categorías diferentes: {total_productos}")

categoria_top = df_tienda['categoria'].value_counts().idxmax()
print(f"4. Categoría más frecuente: {categoria_top}")

print("\nLos gráficos generados permiten visualizar:")
print("- La frecuencia de productos vendidos")
print("- Comparación de promedios")
print("- Tendencias dentro del dataset")