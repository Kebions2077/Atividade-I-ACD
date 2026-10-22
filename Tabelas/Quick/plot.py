
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import unicodedata
import re

# ==================================================
# 1. LOCALIZAR O ARQUIVO ODS E CRIAR A PASTA
# ==================================================

PASTA = Path(__file__).resolve().parent

PASTA_GRAFICOS = PASTA / "graficos"
PASTA_GRAFICOS.mkdir(parents=True, exist_ok=True)

# Procura o arquivo BenchmarkQuick.ods
arquivos_ods = [
    arquivo for arquivo in PASTA.glob("*.ods")
    if not arquivo.name.startswith("~$")
]

arquivo_ods = next(
    (
        arquivo for arquivo in arquivos_ods
        if arquivo.name.lower() == "benchmarkquick.ods"
    ),
    None
)

# Caso o arquivo tenha outro nome, procura Quick no nome
if arquivo_ods is None:
    arquivos_quick = [
        arquivo for arquivo in arquivos_ods
        if "quick" in arquivo.name.lower()
    ]

    if arquivos_quick:
        arquivo_ods = arquivos_quick[0]
    elif arquivos_ods:
        arquivo_ods = max(
            arquivos_ods,
            key=lambda arquivo: arquivo.stat().st_mtime
        )
    else:
        raise FileNotFoundError(
            f"Nenhum arquivo .ods encontrado em: {PASTA}"
        )

print(f"Arquivo encontrado: {arquivo_ods.name}")
print(f"Pasta dos gráficos: {PASTA_GRAFICOS}")

# ==================================================
# 2. LER A PLANILHA
# ==================================================

df = pd.read_excel(arquivo_ods, engine="odf")

coluna_tamanho = "Tamanho (N)"
coluna_media = "MÉDIA (ms)"

colunas_execucao = [
    coluna for coluna in df.columns
    if str(coluna).strip().startswith("Exec ")
]

if coluna_tamanho not in df.columns:
    raise ValueError(
        f"Coluna '{coluna_tamanho}' não encontrada."
    )

if coluna_media not in df.columns:
    raise ValueError(
        f"Coluna '{coluna_media}' não encontrada."
    )

if not colunas_execucao:
    raise ValueError(
        "Nenhuma coluna de execução foi encontrada."
    )

# ==================================================
# 3. SEPARAR OS CENÁRIOS
# ==================================================

cenarios = {}
cenario_atual = None

for _, linha in df.iterrows():

    valor = linha[coluna_tamanho]

    # Linhas de texto indicam o nome do cenário
    if isinstance(valor, str):
        nome = valor.strip()

        if nome:
            cenario_atual = nome
            cenarios[cenario_atual] = []

        continue

    # Linhas numéricas contêm os resultados
    if cenario_atual is not None and pd.notna(valor):
        cenarios[cenario_atual].append(linha.to_dict())

# Converter cada cenário em DataFrame
cenarios_validos = {}

for nome, registros in cenarios.items():

    dados = pd.DataFrame(registros)

    if dados.empty:
        continue

    dados[coluna_tamanho] = pd.to_numeric(
        dados[coluna_tamanho],
        errors="coerce"
    )

    dados[coluna_media] = pd.to_numeric(
        dados[coluna_media],
        errors="coerce"
    )

    dados = dados.dropna(
        subset=[coluna_tamanho, coluna_media]
    )

    dados = dados.sort_values(coluna_tamanho)

    if not dados.empty:
        cenarios_validos[nome] = dados

cenarios = cenarios_validos

if not cenarios:
    raise ValueError(
        "Nenhum cenário com dados válidos foi encontrado."
    )

# ==================================================
# 4. NORMALIZAR NOMES DOS ARQUIVOS
# ==================================================

def nome_seguro(texto):
    texto = unicodedata.normalize("NFKD", texto)
    texto = texto.encode("ascii", "ignore").decode("ascii")
    texto = texto.lower()
    texto = re.sub(r"[^a-z0-9]+", "_", texto)
    return texto.strip("_")

# ==================================================
# 5. GRÁFICOS INDIVIDUAIS
# ==================================================

for nome, dados in cenarios.items():

    x = dados[coluna_tamanho].to_numpy(dtype=float)
    media = dados[coluna_media].to_numpy(dtype=float)

    # Calcular o desvio-padrão das execuções
    execucoes = dados[colunas_execucao].apply(
        pd.to_numeric,
        errors="coerce"
    )

    desvio = execucoes.std(
        axis=1,
        ddof=1
    ).to_numpy(dtype=float)

    desvio = np.nan_to_num(
        desvio,
        nan=0.0,
        posinf=0.0,
        neginf=0.0
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.errorbar(
        x,
        media,
        yerr=desvio,
        marker="o",
        capsize=4,
        linewidth=2,
        label="Média ± desvio-padrão"
    )

    ax.set_title(
        f"QuickSort — Desempenho ({nome})",
        fontsize=14,
        fontweight="bold"
    )

    ax.set_xlabel("Tamanho da entrada (N)", fontsize=12)
    ax.set_ylabel("Tempo de execução (ms)", fontsize=12)

    ax.set_xscale("log")
    ax.set_yscale("log")

    ax.grid(
        True,
        which="both",
        linestyle="--",
        alpha=0.5
    )

    ax.legend()
    fig.tight_layout()

    destino = (
        PASTA_GRAFICOS
        / f"quicksort_{nome_seguro(nome)}.png"
    )

    fig.savefig(
        destino,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(fig)

    print(f"Gráfico gerado: {destino.name}")

# ==================================================
# 6. GRÁFICO COMPARATIVO DOS CENÁRIOS
# ==================================================

fig, ax = plt.subplots(figsize=(11, 7))

for nome, dados in cenarios.items():

    ax.plot(
        dados[coluna_tamanho],
        dados[coluna_media],
        marker="o",
        linewidth=2,
        label=nome
    )

ax.set_title(
    "QuickSort — Comparação de desempenho por cenário",
    fontsize=14,
    fontweight="bold"
)

ax.set_xlabel("Tamanho da entrada (N)", fontsize=12)
ax.set_ylabel("Tempo médio de execução (ms)", fontsize=12)

ax.set_xscale("log")
ax.set_yscale("log")

ax.grid(
    True,
    which="both",
    linestyle="--",
    alpha=0.5
)

ax.legend()
fig.tight_layout()

destino = PASTA_GRAFICOS / "quicksort_comparativo.png"

fig.savefig(
    destino,
    dpi=300,
    bbox_inches="tight"
)

plt.close(fig)

print(f"Gráfico gerado: {destino.name}")

# ==================================================
# 7. FINALIZAÇÃO
# ==================================================

print("\nTodos os gráficos foram gerados com sucesso!")
print(f"Localização: {PASTA_GRAFICOS}")
