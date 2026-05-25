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

# 🔥 COLUMNAS DE TU TIENDA
DEFAULT_SEXO_COL = "sexo"        # mujer / hombre
DEFAULT_TIPO_COL = "tipo"        # camisetas / pantalones / pijamas / maquillaje
DEFAULT_VENTAS_COL = "ventas"

DEFAULT_OUTPUT_DIR = Path("reportes")


# =========================
# VALIDACIÓN
# =========================
def _validar_dataframe(df):
    if not isinstance(df, pd.DataFrame):
        raise TypeError("El argumento debe ser un pandas.DataFrame")

    if df.empty:
        raise ValueError("El dataframe está vacío")

    df = df.copy()
    df.columns = df.columns.str.strip().str.lower()
    return df


def _normalizar_columna(df, col):
    col = col.strip().lower()
    if col not in df.columns:
        raise KeyError(f"No existe la columna '{col}'")
    return col


# =========================
# UTILIDADES
# =========================
def _guardar_figura(fig, path, formato="svg"):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(path, format=formato, bbox_inches="tight")
    plt.close(fig)
    return path


def _figura_a_base64(fig, formato="png"):
    buffer = BytesIO()
    fig.savefig(buffer, format=formato, bbox_inches="tight")
    buffer.seek(0)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# =========================
# GRÁFICO 1: VENTAS POR SEXO
# =========================
def graficar_ventas_por_sexo(df, sexo_col=DEFAULT_SEXO_COL, ventas_col=DEFAULT_VENTAS_COL):
    df = _validar_dataframe(df)

    sexo_col = _normalizar_columna(df, sexo_col)
    ventas_col = _normalizar_columna(df, ventas_col)

    df[ventas_col] = pd.to_numeric(df[ventas_col], errors="coerce")
    df = df.dropna(subset=[ventas_col])

    data = df.groupby(sexo_col)[ventas_col].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(8, 5))
    sns.barplot(x=data.index, y=data.values, ax=ax, color="#4C72B0")

    ax.set_title("Ventas por categoría (Mujer vs Hombre)")
    ax.set_xlabel("Sexo")
    ax.set_ylabel("Ventas")

    return fig


# =========================
# GRÁFICO 2: VENTAS POR TIPO
# =========================
def graficar_ventas_por_tipo(df, tipo_col=DEFAULT_TIPO_COL, ventas_col=DEFAULT_VENTAS_COL):
    df = _validar_dataframe(df)

    tipo_col = _normalizar_columna(df, tipo_col)
    ventas_col = _normalizar_columna(df, ventas_col)

    df[ventas_col] = pd.to_numeric(df[ventas_col], errors="coerce")
    df = df.dropna(subset=[ventas_col])

    data = df.groupby(tipo_col)[ventas_col].sum().sort_values(ascending=True)

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.barplot(x=data.index, y=data.values, ax=ax, color="#55A868")

    ax.set_title("Ventas por tipo de producto")
    ax.set_xlabel("Tipo")
    ax.set_ylabel("Ventas")
    ax.tick_params(axis="x", rotation=30)

    return fig


# =========================
# REPORTE COMPLETO
# =========================
def generar_reporte(df, output_dir=DEFAULT_OUTPUT_DIR):
    df = _validar_dataframe(df)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    fig_sexo = graficar_ventas_por_sexo(df)
    fig_tipo = graficar_ventas_por_tipo(df)

    ruta_sexo = _guardar_figura(fig_sexo, output_dir / "ventas_sexo.svg")
    ruta_tipo = _guardar_figura(fig_tipo, output_dir / "ventas_tipo.svg")

    return {
        "sexo": {
            "svg": str(ruta_sexo),
            "base64": _figura_a_base64(fig_sexo),
            "titulo": "Ventas por sexo"
        },
        "tipo": {
            "svg": str(ruta_tipo),
            "base64": _figura_a_base64(fig_tipo),
            "titulo": "Ventas por tipo"
        }
    }


# =========================
# CARGA CSV
# =========================
def cargar_csv(path):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError("No existe el archivo CSV")
    return pd.read_csv(path)


# =========================
# MAIN
# =========================
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", required=True)
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT_DIR))

    args = parser.parse_args()

    df = cargar_csv(args.csv)
    reporte = generar_reporte(df, args.output)

    print("✅ Reporte generado")
    print("Sexo:", reporte["sexo"]["svg"])
    print("Tipo:", reporte["tipo"]["svg"])


if __name__ == "__main__":
    main()