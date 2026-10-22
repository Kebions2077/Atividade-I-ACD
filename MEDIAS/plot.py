
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

# Diretório onde este algoritmo Python está salvo
INPUT_DIR = Path(__file__).resolve().parent

# Pasta onde os gráficos serão salvos
PASTA_GRAFICOS = INPUT_DIR / "graficos"

# Arquivos e nomes dos gráficos
ARQUIVOS = {
    "Aleatorio.ods": "Aleatorio",
    "Cresente.ods": "Crescente",
    "Decrescente.ods": "Decrescente",
    "Repetido.ods": "Repetido",
}


def limpar_dados(df: pd.DataFrame) -> pd.DataFrame:
    """Converte os dados para valores numéricos."""
    df = df.copy()
    df = df.rename(columns={df.columns[0]: "Algoritmo"})

    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def plotar_grafico(df: pd.DataFrame, titulo: str, pasta: Path):
    """Cria e salva os gráficos em PNG e PDF."""
    algoritmos = df["Algoritmo"].tolist()
    tamanhos = [str(c) for c in df.columns[1:]]

    dados = df.set_index("Algoritmo")[df.columns[1:]].values.T

    x = np.arange(len(algoritmos))
    largura = 0.18
    cores = plt.cm.tab10(np.linspace(0, 1, len(tamanhos)))

    fig, ax = plt.subplots(figsize=(14, 7))

    for i, (tamanho, cor) in enumerate(zip(tamanhos, cores)):
        offset = (i - len(tamanhos) / 2) * largura + largura / 2

        barras = ax.bar(
            x + offset,
            dados[i],
            largura,
            label=f"n = {tamanho}",
            color=cor
        )

        for barra, valor in zip(barras, dados[i]):
            if not np.isnan(valor) and valor > 0:
                altura = barra.get_height()

                ax.annotate(
                    f"{valor:.1f}" if valor < 1000 else f"{valor:.0f}",
                    xy=(barra.get_x() + barra.get_width() / 2, altura),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha="center",
                    va="bottom",
                    fontsize=7,
                    rotation=90
                )

    ax.set_ylabel("Tempo (ms ou unidade do experimento)")
    ax.set_title(titulo, fontsize=14, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(algoritmos, rotation=45, ha="right")
    ax.legend(title="Tamanho da entrada")
    ax.set_yscale("log")
    ax.grid(axis="y", linestyle="--", alpha=0.7)

    plt.tight_layout()

    # Salva os gráficos dentro da pasta graficos
    nome_arquivo = titulo.replace("–", "-").replace(" ", "_")

    caminho_png = pasta / f"{nome_arquivo}.png"
    caminho_pdf = pasta / f"{nome_arquivo}.pdf"

    fig.savefig(caminho_png, dpi=150, bbox_inches="tight")
    fig.savefig(caminho_pdf, bbox_inches="tight")

    plt.close(fig)

    print(f"  Gráfico PNG salvo em: {caminho_png}")
    print(f"  Gráfico PDF salvo em: {caminho_pdf}")


def main():
    # Cria a pasta graficos no diretório do algoritmo
    PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

    print(f"Diretório do algoritmo: {INPUT_DIR}")
    print(f"Pasta dos gráficos: {PASTA_GRAFICOS}")
    print()

    for arquivo, nome in ARQUIVOS.items():
        caminho = INPUT_DIR / arquivo

        if not caminho.exists():
            print(f"[AVISO] Arquivo não encontrado: {caminho}")
            continue

        print(f"Processando: {arquivo}")

        try:
            # Lê o arquivo ODS
            df = pd.read_excel(caminho, engine="odf")
            df = limpar_dados(df)

            # Gera os gráficos
            titulo = f"Tempos de ordenação - {nome}"
            plotar_grafico(df, titulo, PASTA_GRAFICOS)

        except Exception as erro:
            print(f"[ERRO] Falha ao processar {arquivo}: {erro}")

    print("\nProcessamento concluído!")
    print(f"Gráficos salvos em: {PASTA_GRAFICOS.resolve()}")


if __name__ == "__main__":
    main()
