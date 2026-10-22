
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta onde o arquivo .py está
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Pasta onde os gráficos serão salvos
PASTA_GRAFICOS = os.path.join(PASTA_SCRIPT, "graficos")


# ============================================================
# ENCONTRAR O ARQUIVO ODS
# ============================================================

def encontrar_ods():

    arquivos = [
        arquivo
        for arquivo in os.listdir(PASTA_SCRIPT)
        if arquivo.lower().endswith(".ods")
        and not arquivo.startswith("~$")
    ]

    if not arquivos:
        print("ERRO: Nenhum arquivo .ods encontrado.")
        print(f"Coloque o arquivo .ods em:")
        print(PASTA_SCRIPT)
        sys.exit(1)

    # Se houver apenas um ODS, usa automaticamente
    if len(arquivos) == 1:
        caminho = os.path.join(PASTA_SCRIPT, arquivos[0])

        print(f"Arquivo encontrado: {arquivos[0]}")

        return caminho

    # Se houver vários, permite escolher
    print("Foram encontrados vários arquivos .ods:\n")

    for i, arquivo in enumerate(arquivos, 1):
        print(f"{i} - {arquivo}")

    while True:
        try:
            escolha = int(input("\nEscolha o arquivo: "))

            if 1 <= escolha <= len(arquivos):
                break

        except ValueError:
            pass

        print("Escolha inválida.")

    return os.path.join(
        PASTA_SCRIPT,
        arquivos[escolha - 1]
    )


# ============================================================
# LER O BENCHMARK
# ============================================================

def ler_benchmark(caminho):

    # Lê a primeira planilha
    df = pd.read_excel(
        caminho,
        engine="odf",
        sheet_name=0,
        header=None
    )

    dados = {}

    categoria_atual = None

    for i in range(len(df)):

        primeira_coluna = df.iloc[i, 0]

        if pd.isna(primeira_coluna):
            continue

        texto = str(primeira_coluna).strip()

        # ----------------------------------------------------
        # Detectar categoria
        # ----------------------------------------------------

        if texto.startswith("Ordem "):

            categoria_atual = texto

            dados[categoria_atual] = []

            continue

        # ----------------------------------------------------
        # Ignorar cabeçalho
        # ----------------------------------------------------

        if texto == "Tamanho (N)":
            continue

        # ----------------------------------------------------
        # Tentar identificar N
        # ----------------------------------------------------

        try:
            tamanho = int(float(primeira_coluna))
        except (ValueError, TypeError):
            continue

        if categoria_atual is None:
            continue

        # ----------------------------------------------------
        # Execuções
        # ----------------------------------------------------

        execucoes = []

        for coluna in range(1, 11):

            valor = df.iloc[i, coluna]

            if pd.notna(valor):

                try:
                    execucoes.append(float(valor))
                except (ValueError, TypeError):
                    pass

        # ----------------------------------------------------
        # Média
        # ----------------------------------------------------

        try:
            media = float(df.iloc[i, 11])
        except (ValueError, TypeError):
            media = sum(execucoes) / len(execucoes)

        dados[categoria_atual].append({
            "tamanho": tamanho,
            "execucoes": execucoes,
            "media": media
        })

    return dados


# ============================================================
# CRIAR PASTA DE SAÍDA
# ============================================================

def criar_pasta():

    os.makedirs(
        PASTA_GRAFICOS,
        exist_ok=True
    )


# ============================================================
# GRÁFICO 1
# COMPARAÇÃO GERAL
# ============================================================

def grafico_comparativo(dados):

    plt.figure(figsize=(11, 7))

    for categoria, valores in dados.items():

        tamanhos = [
            item["tamanho"]
            for item in valores
        ]

        medias = [
            item["media"]
            for item in valores
        ]

        nome = categoria.replace(
            "Ordem ",
            ""
        )

        plt.plot(
            tamanhos,
            medias,
            marker="o",
            linewidth=2,
            label=nome
        )

    plt.xlabel("Tamanho da entrada (N)")
    plt.ylabel("Tempo médio (ms)")

    plt.title(
        "Bucket Sort - Comparação do tempo médio"
    )

    plt.xscale("log")
    plt.yscale("log")

    plt.grid(
        True,
        which="both",
        linestyle="--",
        alpha=0.5
    )

    plt.legend()

    plt.tight_layout()

    caminho = os.path.join(
        PASTA_GRAFICOS,
        "01_comparativo_geral.png"
    )

    plt.savefig(
        caminho,
        dpi=300
    )

    plt.show()
    plt.close()

    print(f"Gerado: {caminho}")


# ============================================================
# GRÁFICO 2
# UM GRÁFICO PARA CADA ORDEM
# ============================================================

def graficos_por_categoria(dados):

    for categoria, valores in dados.items():

        tamanhos = [
            item["tamanho"]
            for item in valores
        ]

        medias = [
            item["media"]
            for item in valores
        ]

        nome = categoria.replace(
            "Ordem ",
            ""
        )

        plt.figure(figsize=(10, 6))

        plt.plot(
            tamanhos,
            medias,
            marker="o",
            linewidth=2
        )

        plt.xlabel("Tamanho da entrada (N)")
        plt.ylabel("Tempo médio (ms)")

        plt.title(
            f"Bucket Sort - {nome}"
        )

        plt.xscale("log")
        plt.yscale("log")

        plt.grid(
            True,
            which="both",
            linestyle="--",
            alpha=0.5
        )

        plt.tight_layout()

        nome_arquivo = (
            nome
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        caminho = os.path.join(
            PASTA_GRAFICOS,
            f"02_{nome_arquivo}.png"
        )

        plt.savefig(
            caminho,
            dpi=300
        )

        plt.show()
        plt.close()

        print(f"Gerado: {caminho}")


# ============================================================
# GRÁFICO 3
# COMPARAÇÃO POR TAMANHO
# ============================================================

def graficos_por_tamanho(dados):

    tamanhos = sorted({
        item["tamanho"]
        for valores in dados.values()
        for item in valores
    })

    for tamanho in tamanhos:

        categorias = []
        medias = []

        for categoria, valores in dados.items():

            for item in valores:

                if item["tamanho"] == tamanho:

                    categorias.append(
                        categoria.replace(
                            "Ordem ",
                            ""
                        )
                    )

                    medias.append(
                        item["media"]
                    )

        plt.figure(figsize=(11, 7))

        plt.bar(
            categorias,
            medias
        )

        plt.xlabel("Tipo de entrada")
        plt.ylabel("Tempo médio (ms)")

        plt.title(
            f"Bucket Sort - Comparação para N = {tamanho:,}"
        )

        plt.yscale("log")

        plt.xticks(
            rotation=25,
            ha="right"
        )

        plt.grid(
            axis="y",
            linestyle="--",
            alpha=0.5
        )

        plt.tight_layout()

        caminho = os.path.join(
            PASTA_GRAFICOS,
            f"03_comparacao_N_{tamanho}.png"
        )

        plt.savefig(
            caminho,
            dpi=300
        )

        plt.show()
        plt.close()

        print(f"Gerado: {caminho}")


# ============================================================
# GRÁFICO 4
# TODAS AS EXECUÇÕES
# ============================================================

def graficos_execucoes(dados):

    for categoria, valores in dados.items():

        nome_categoria = categoria.replace(
            "Ordem ",
            ""
        )

        for item in valores:

            execucoes = item["execucoes"]

            if not execucoes:
                continue

            numero_execucao = range(
                1,
                len(execucoes) + 1
            )

            plt.figure(figsize=(10, 6))

            plt.plot(
                numero_execucao,
                execucoes,
                marker="o"
            )

            # Linha da média
            plt.axhline(
                item["media"],
                linestyle="--",
                label=f"Média = {item['media']:.3f} ms"
            )

            plt.xlabel("Número da execução")
            plt.ylabel("Tempo (ms)")

            plt.title(
                f"Bucket Sort - {nome_categoria} - "
                f"N = {item['tamanho']:,}"
            )

            plt.xticks(
                range(1, len(execucoes) + 1)
            )

            plt.grid(
                True,
                linestyle="--",
                alpha=0.5
            )

            plt.legend()

            plt.tight_layout()

            nome_arquivo = (
                nome_categoria
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            caminho = os.path.join(
                PASTA_GRAFICOS,
                f"04_execucoes_{nome_arquivo}"
                f"_N_{item['tamanho']}.png"
            )

            plt.savefig(
                caminho,
                dpi=300
            )

            plt.show()
            plt.close()


# ============================================================
# GRÁFICO 5
# VARIAÇÃO ENTRE AS EXECUÇÕES
# ============================================================

def grafico_variacao(dados):

    for categoria, valores in dados.items():

        nomes = []
        medias = []
        minimos = []
        maximos = []

        for item in valores:

            nomes.append(
                f"N={item['tamanho']:,}"
            )

            medias.append(
                item["media"]
            )

            minimos.append(
                min(item["execucoes"])
            )

            maximos.append(
                max(item["execucoes"])
            )

        plt.figure(figsize=(11, 7))

        plt.errorbar(
            nomes,
            medias,
            yerr=[
                [
                    media - minimo
                    for media, minimo
                    in zip(medias, minimos)
                ],
                [
                    maximo - media
                    for media, maximo
                    in zip(medias, maximos)
                ]
            ],
            marker="o",
            linestyle="-",
            capsize=5
        )

        plt.xlabel("Tamanho da entrada")
        plt.ylabel("Tempo (ms)")

        plt.title(
            f"Bucket Sort - Variação das execuções - "
            f"{categoria}"
        )

        plt.yscale("log")

        plt.grid(
            True,
            which="both",
            linestyle="--",
            alpha=0.5
        )

        plt.tight_layout()

        nome = (
            categoria
            .replace("Ordem ", "")
            .replace(" ", "_")
        )

        caminho = os.path.join(
            PASTA_GRAFICOS,
            f"05_variacao_{nome}.png"
        )

        plt.savefig(
            caminho,
            dpi=300
        )

        plt.show()
        plt.close()


# ============================================================
# MOSTRAR RESUMO
# ============================================================

def mostrar_resumo(dados):

    print("\n")
    print("=" * 70)
    print("DADOS ENCONTRADOS")
    print("=" * 70)

    for categoria, valores in dados.items():

        print(f"\n{categoria}")

        for item in valores:

            print(
                f"N = {item['tamanho']:,} | "
                f"Média = {item['media']:.3f} ms | "
                f"Execuções = {len(item['execucoes'])}"
            )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 70)
    print("GERADOR DE GRÁFICOS - BUCKET SORT")
    print("=" * 70)

    # Encontrar ODS
    caminho = encontrar_ods()

    # Ler dados
    dados = ler_benchmark(caminho)

    if not dados:

        print(
            "\nERRO: Nenhum dado de benchmark "
            "foi encontrado no arquivo."
        )

        sys.exit(1)

    # Criar pasta
    criar_pasta()

    # Mostrar resumo
    mostrar_resumo(dados)

    print("\n")
    print("=" * 70)
    print("GERANDO GRÁFICOS")
    print("=" * 70)

    # Gráficos
    grafico_comparativo(dados)

    graficos_por_categoria(dados)

    graficos_por_tamanho(dados)

    graficos_execucoes(dados)

    grafico_variacao(dados)

    print("\n")
    print("=" * 70)
    print("FINALIZADO!")
    print("=" * 70)

    print(
        f"\nOs gráficos foram salvos em:\n"
        f"{PASTA_GRAFICOS}"
    )


# ============================================================
# EXECUTAR
# ============================================================

if __name__ == "__main__":
    main()
