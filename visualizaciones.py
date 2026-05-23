# -*- coding: utf-8 -*-
import argparse
import base64
from io import BytesIO
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

DEFAULT_CATEGORIA_COL = "categoria"
DEFAULT_VALOR_COL = "ventas"
DEFAULT_OUTPUT_DIR = Path("reportes")


def _validar_dataframe(dataframe):
    if not isinstance(dataframe, pd.DataFrame):
        raise TypeError("El argumento dataframe debe ser un pandas.DataFrame")

    if dataframe.empty:
        raise ValueError("El dataframe no puede estar vacío")

    return dataframe.copy()


def _guardar_figura(figura, output_path, formato="svg"):
    ruta = Path(output_path)
    ruta.parent.mkdir(parents=True, exist_ok=True)
    figura.savefig(ruta, format=formato, bbox_inches="tight")
    return ruta


def _figura_a_base64(figura, formato="png"):
    buffer = BytesIO()
    figura.savefig(buffer, format=formato, bbox_inches="tight")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


def _normalizar_columna(dataframe, columna):
    if columna not in dataframe.columns:
        raise KeyError(f"La columna '{columna}' no existe en el dataframe")
    return columna


def graficar_frecuencia(dataframe, columna=DEFAULT_CATEGORIA_COL, top_n=8):
    """Genera un gráfico de barras con los elementos más frecuentes."""
    df = _validar_dataframe(dataframe)
    columna = _normalizar_columna(df, columna)

    conteo = df[columna].value_counts().head(top_n)

    figura, eje = plt.subplots(figsize=(10, 5))
    sns.barplot(x=conteo.index, y=conteo.values, ax=eje, color="#4C72B0")

    eje.set_title(f"Frecuencia de {columna}")
    eje.set_xlabel(columna)
    eje.set_ylabel("Cantidad")
    eje.tick_params(axis="x", rotation=30)

    return figura


def graficar_promedios(dataframe, categoria_col=DEFAULT_CATEGORIA_COL, valor_col=DEFAULT_VALOR_COL):
    """Genera un gráfico de barras con el promedio por categoría."""
    df = _validar_dataframe(dataframe)
    categoria_col = _normalizar_columna(df, categoria_col)
    valor_col = _normalizar_columna(df, valor_col)

    df[valor_col] = pd.to_numeric(df[valor_col], errors="coerce")
    df = df.dropna(subset=[valor_col])

    if df.empty:
        raise ValueError(f"La columna '{valor_col}' no contiene valores numéricos válidos")

    promedio = df.groupby(categoria_col)[valor_col].mean().sort_values(ascending=False)

    figura, eje = plt.subplots(figsize=(10, 5))
    sns.barplot(x=promedio.index, y=promedio.values, ax=eje, color="#55A868")

    eje.set_title(f"Promedio de {valor_col} por {categoria_col}")
    eje.set_xlabel(categoria_col)
    eje.set_ylabel(f"Promedio de {valor_col}")
    eje.tick_params(axis="x", rotation=30)

    return figura


def generar_reporte_visual(
    dataframe,
    output_dir=DEFAULT_OUTPUT_DIR,
    categoria_col=DEFAULT_CATEGORIA_COL,
    valor_col=DEFAULT_VALOR_COL,
    top_n=8,
):
    """Genera gráficas, las guarda como SVG y devuelve su representación base64."""
    df = _validar_dataframe(dataframe)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    figura_frecuencia = graficar_frecuencia(df, columna=categoria_col, top_n=top_n)
    figura_promedios = graficar_promedios(df, categoria_col=categoria_col, valor_col=valor_col)

    ruta_frecuencia = _guardar_figura(figura_frecuencia, output_dir / "frecuencia.svg", formato="svg")
    ruta_promedios = _guardar_figura(figura_promedios, output_dir / "promedios.svg", formato="svg")

    reporte = {
        "frecuencia": {
            "svg": str(ruta_frecuencia),
            "base64_png": _figura_a_base64(figura_frecuencia, formato="png"),
            "titulo": f"Frecuencia de {categoria_col}",
        },
        "promedios": {
            "svg": str(ruta_promedios),
            "base64_png": _figura_a_base64(figura_promedios, formato="png"),
            "titulo": f"Promedio de {valor_col} por {categoria_col}",
        },
    }

    return reporte


def cargar_datos_csv(ruta_csv):
    """Carga un CSV limpio y lo convierte en dataframe listo para visualizar."""
    ruta = Path(ruta_csv)
    if not ruta.exists():
        raise FileNotFoundError(f"No se encontró el archivo: {ruta}")

    return pd.read_csv(ruta)


def main():
    parser = argparse.ArgumentParser(
        description="Genera visualizaciones y reportes SVG/base64 a partir de un CSV limpio."
    )
    parser.add_argument("--csv", required=True, help="Ruta al archivo CSV limpio")
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT_DIR),
        help="Directorio donde guardar los archivos SVG",
    )
    parser.add_argument(
        "--categoria-col",
        default=DEFAULT_CATEGORIA_COL,
        help="Nombre de la columna categórica",
    )
    parser.add_argument(
        "--valor-col",
        default=DEFAULT_VALOR_COL,
        help="Nombre de la columna numérica a promediar",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=8,
        help="Número de categorías a mostrar en el gráfico de frecuencia",
    )

    args = parser.parse_args()

    dataframe = cargar_datos_csv(args.csv)
    reporte = generar_reporte_visual(
        dataframe,
        output_dir=args.output,
        categoria_col=args.categoria_col,
        valor_col=args.valor_col,
        top_n=args.top_n,
    )

    print("Reporte generado correctamente")
    print(f"Frecuencia: {reporte['frecuencia']['svg']}")
    print(f"Promedios: {reporte['promedios']['svg']}")
    print("Usa el campo base64_png en React para renderizar la imagen.")


if __name__ == "__main__":
    main()
