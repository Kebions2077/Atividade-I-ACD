from pathlib import Path
import re
import sys
import pandas as pd
import matplotlib.pyplot as plt

PASTA_SCRIPT = Path(__file__).resolve().parent
PASTA_SAIDA = PASTA_SCRIPT / "graficos_mergesort"
PASTA_SAIDA.mkdir(exist_ok=True)

def encontrar_arquivo_ods():
    arquivos = sorted(
        p for p in PASTA_SCRIPT.glob("*.ods")
        if not p.name.startswith("~$")
    )
    if not arquivos:
        raise FileNotFoundError(
            f"Nenhum arquivo .ods encontrado na pasta: {PASTA_SCRIPT}"
        )
    preferidos = [p for p in arquivos if "merge" in p.stem.lower()]
    candidatos = preferidos or arquivos
    if len(candidatos) == 1:
        return candidatos[0]
    print("Arquivos ODS encontrados:")
    for i, p in enumerate(candidatos, 1):
        print(f"  {i}. {p.name}")
    try:
        return candidatos[int(input("Escolha o número do arquivo: ").strip()) - 1]
    except (ValueError, IndexError):
        raise ValueError("Seleção inválida.")

def nome_seguro(texto):
    return re.sub(r"[^\w\-]+", "_", str(texto), flags=re.UNICODE).strip("_")

def ler_dados(arquivo):
    df = pd.read_excel(arquivo, sheet_name=0, header=None, engine="odf")
    secoes = {}
    secao = None

    for _, linha in df.iterrows():
        primeira = linha.iloc[0]
        if isinstance(primeira, str):
            texto = primeira.strip()
            if texto.lower().startswith("ordem ") or texto.lower() == "elementos repetidos":
                secao = texto
                secoes.setdefault(secao, [])
                continue

        try:
            n = int(float(primeira))
        except (TypeError, ValueError, OverflowError):
            continue

        if secao is None:
            continue

        execucoes = pd.to_numeric(linha.iloc[1:11], errors="coerce").dropna().astype(float).tolist()
        media = pd.to_numeric(pd.Series([linha.iloc[11]]), errors="coerce").iloc[0]
        if pd.isna(media):
            if not execucoes:
                continue
            media = sum(execucoes) / len(execucoes)

        secoes[secao].append({
            "N": n,
            "media": float(media),
            "execucoes": execucoes
        })

    for nome in secoes:
        secoes[nome] = sorted(secoes[nome], key=lambda x: x["N"])
    return {k: v for k, v in secoes.items() if v}

def gerar_graficos(secoes):
    if not secoes:
        raise ValueError("Não foram encontrados dados reconhecíveis na planilha.")

    # Um gráfico de tempo médio por cenário
    for nome, linhas in secoes.items():
        xs = [r["N"] for r in linhas]
        ys = [r["media"] for r in linhas]
        plt.figure(figsize=(9, 5))
        plt.plot(xs, ys, marker="o", linewidth=2)
        plt.xscale("log")
        if all(y > 0 for y in ys):
            plt.yscale("log")
        plt.title(f"Merge Sort — {nome}")
        plt.xlabel("Tamanho da entrada (N)")
        plt.ylabel("Tempo médio (ms)")
        plt.grid(True, which="both", linestyle="--", alpha=0.35)
        plt.tight_layout()
        destino = PASTA_SAIDA / f"{nome_seguro(nome)}.png"
        plt.savefig(destino, dpi=160)
        plt.close()
        print(f"Gráfico salvo: {destino.name}")
