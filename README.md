# Momento 3 - Visualizaciones y Reportes

Este proyecto ahora incluye un módulo para generar visualizaciones, exportarlas como SVG y convertirlas a Base64 para su uso en React.

## Resultados

El reporte generado con datos de moda muestra dos gráficas principales:

1. **Frecuencia**: identifica las categorías de moda más comunes del dataset.
2. **Promedios**: compara el promedio de ventas por categoría.

Estas gráficas se guardan en la carpeta `reportes/` y también pueden usarse como Base64 desde Python o desde un componente de React.

## Resultados y Análisis Visual

El análisis que realizamos nos permitió descubrir cuáles son los productos más vendidos, las categorías que aparecen con más frecuencia y los promedios generales de precios.

Los gráficos que generamos son una gran ayuda para visualizar los datos que obtuvimos del archivo CSV limpio, lo que hace mucho más fácil identificar patrones y tendencias en la información que analizamos.

## Requisitos

Instala las dependencias necesarias con:

```bash
pip install pandas matplotlib seaborn
```

## Cómo ejecutar el script

El CSV de ejemplo ya está preparado para el dominio de moda. Ejecuta:

```bash
python visualizaciones.py --csv sample_reporte.csv --output reportes
```

Si usas tu propio CSV limpio, también puedes hacerlo así:

```bash
python visualizaciones.py --csv datos_limpios.csv --output reportes
```

También puedes utilizar el módulo directamente desde Python:

```python
from visualizaciones import cargar_datos_csv, generar_reporte_visual


df = cargar_datos_csv("sample_reporte.csv")
reporte = generar_reporte_visual(df, output_dir="reportes")

print(reporte["frecuencia"]["svg"])
print(reporte["promedios"]["svg"])
```

## Integración con React

El reporte devuelve una cadena Base64 en `base64_png`, lista para mostrarse en un `<img>`:

```jsx
function Grafico({ base64 }) {
  return <img src={`data:image/png;base64,${base64}`} alt="Gráfico generado" />;
}
```

Si ya tienes el JSON del reporte, puedes pasar `reporte.frecuencia.base64_png` o `reporte.promedios.base64_png` al componente.

## Archivos generados

- `reportes/frecuencia.svg`
- `reportes/promedios.svg`

Estos archivos son la versión exportada del reporte y pueden consultarse directamente en el front-end.
