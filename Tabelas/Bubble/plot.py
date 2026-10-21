
import os
import sys
import pandas as pd
import matplotlib.pyplot as plt


# ============================================================
# CONFIGURAÇÕES
# ============================================================

# Pasta onde este arquivo .py está localizado
PASTA_SCRIPT = os.path.dirname(os.path.abspath(__file__))

# Extensão que será procurada
EXTENSAO = ".ods"

# Pasta onde os gráficos serão salvos
PASTA_GRAFICOS = os.path.join(PASTA_SCRIPT, "graficos")


# ============================================================
# LOCALIZAR O ARQUIVO ODS
# ============================================================

def encontrar_ods():
    """
    Procura arquivos .ods na mesma pasta do programa.
    Ignora arquivos que comecem com '~$'.
    """

    arquivos = [
        arquivo
        for arquivo in os.listdir(PASTA_SCRIPT)
        if arquivo.lower().endswith(EXTENSAO)
        and not arquivo.startswith("~$")
    ]

    if not arquivos:
        print("ERRO: Nenhum arquivo .ods foi encontrado.")
        print(f"Coloque o arquivo .ods na pasta:")
        print(PASTA_SCRIPT)
        sys.exit(1)

    if len(arquivos) > 1:
        print("Foram encontrados vários arquivos .ods:")
        for i, arquivo in enumerate(arquivos, 1):
            print(f"  {i} - {arquivo}")

        escolha = input("Digite o número do arquivo que deseja utilizar: ")

        try:
            escolha = int(escolha) - 1
            arquivo_escolhido = arquivos[escolha]
        except (ValueError, IndexError):
            print("Escolha inválida.")
            sys.exit(1)
    else:
        arquivo_escolhido = arquivos[0]

    caminho = os.path.join(PASTA_SCRIPT, arquivo_escolhido)

    print(f"Arquivo encontrado: {arquivo_escolhido}")

    return caminho


# ============================================================
# LER OS DADOS DO ODS
# ============================================================

def ler_benchmark(caminho):
    """
    Lê a planilha e identifica automaticamente as seções
    do benchmark.
    """

    df = pd.read_excel(
        caminho,
        engine="odf",
        sheet_name=0,
        header=None
    )

    dados = {}

    categoria_atual = None

    for _, linha in df.iterrows():

        primeira_coluna = linha.iloc[0]

        # Ignora linhas completamente vazias
        if pd.isna(primeira_coluna):
            continue

        valor = str(primeira_coluna).strip()

        # ----------------------------------------------------
        # Detecta uma nova categoria
        # ----------------------------------------------------

        if valor.startswith("Ordem "):

            categoria_atual = valor

            dados[categoria_atual] = []

            continue

        # ----------------------------------------------------
        # Detecta uma linha de dados
        # ----------------------------------------------------

        try:
            tamanho = int(float(primeira_coluna))
        except (ValueError, TypeError):
            continue

        if categoria_atual is None:
            continue

        # Média está na última coluna
        media = linha.iloc[-1]

        try:
            media = float(media)
        except (ValueError, TypeError):
            continue

        # Guarda também todas as execuções
        execucoes = []

        for valor_execucao in linha.iloc[1:-1]:

            if pd.notna(valor_execucao):

                try:
                    execucoes.append(float(valor_execucao))
                except (ValueError, TypeError):
                    pass

        dados[categoria_atual].append({
            "tamanho": tamanho,
            "media": media,
            "execucoes": execucoes
        })

    return dados


# ============================================================
# CRIAR PASTA DOS GRÁFICOS
# ============================================================

def criar_pasta_graficos():

    os.makedirs(PASTA_GRAFICOS, exist_ok=True)

    print(f"Pasta dos gráficos: {PASTA_GRAFICOS}")


# ============================================================
# GRÁFICO 1
# MÉDIA POR TAMANHO PARA CADA TIPO DE ENTRADA
# ============================================================

def grafico_comparativo(dados):

    plt.figure(figsize=(11, 7))

    for categoria, valores in dados.items():

        if not valores:
            continue

        tamanhos = [item["tamanho"] for item in valores]
        medias = [item["media"] for item in valores]

        plt.plot(
            tamanhos,
            medias,
            marker="o",
            linewidth=2,
            label=categoria.replace("Ordem ", "")
        )

    plt.xlabel("Tamanho da entrada (N)")
    plt.ylabel("Tempo médio (ms)")
    plt.title("Bubble Sort - Tempo médio por tamanho da entrada")

    plt.xscale("log")
    plt.yscale("log")

    plt.grid(True, which="both", linestyle="--", alpha=0.5)
    plt.legend()

    plt.tight_layout()

    caminho = os.path.join(
        PASTA_GRAFICOS,
        "01_comparativo_geral.png"
    )

    plt.savefig(caminho, dpi=300)
    plt.show()
    plt.close()

    print(f"Gráfico salvo: {caminho}")


# ============================================================
# GRÁFICOS INDIVIDUAIS
# ============================================================

def graficos_individuais(dados):

    for categoria, valores in dados.items():

        if not valores:
            continue

        tamanhos = [item["tamanho"] for item in valores]
        medias = [item["media"] for item in valores]

        plt.figure(figsize=(10, 6))

        plt.plot(
            tamanhos,
            medias,
            marker="o",
            linewidth=2
        )

        plt.xlabel("Tamanho da entrada (N)")
        plt.ylabel("Tempo médio (ms)")

        titulo = f"Bubble Sort - {categoria}"

        plt.title(titulo)

        plt.xscale("log")
        plt.yscale("log")

        plt.grid(True, which="both", linestyle="--", alpha=0.5)

        plt.tight_layout()

        # Remove caracteres problemáticos do nome do arquivo
        nome_arquivo = (
            categoria
            .replace("Ordem ", "")
            .replace(" ", "_")
            .replace("/", "_")
            .replace("\\", "_")
        )

        caminho = os.path.join(
            PASTA_GRAFICOS,
            f"{nome_arquivo}.png"
        )

        plt.savefig(caminho, dpi=300)
        plt.show()
        plt.close()

        print(f"Gráfico salvo: {caminho}")


# ============================================================
# GRÁFICO DE BARRAS
# COMPARAÇÃO PARA CADA TAMANHO
# ============================================================

def grafico_barras(dados):

    # Obtém todos os tamanhos existentes
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
                        categoria.replace("Ordem ", "")
                    )

                    medias.append(item["media"])

        if not categorias:
            continue

        plt.figure(figsize=(12, 7))

        plt.bar(categorias, medias)

        plt.xlabel("Tipo de entrada")
        plt.ylabel("Tempo médio (ms)")

        plt.title(
            f"Bubble Sort - Comparação para N = {tamanho:,}"
        )

        plt.xticks(rotation=30, ha="right")

        # Escala log ajuda quando os tempos têm grande diferença
        plt.yscale("log")

        plt.grid(
            axis="y",
            linestyle="--",
            alpha=0.5
        )

        plt.tight_layout()

        caminho = os.path.join(
            PASTA_GRAFICOS,
            f"02_comparacao_N_{tamanho}.png"
        )

        plt.savefig(caminho, dpi=300)
        plt.show()
        plt.close()

        print(f"Gráfico salvo: {caminho}")


# ============================================================
# GRÁFICO DAS EXECUÇÕES INDIVIDUAIS
# ============================================================

def grafico_execucoes(dados):

    for categoria, valores in dados.items():

        for item in valores:

            execucoes = item["execucoes"]

            if not execucoes:
                continue

            plt.figure(figsize=(10, 6))

            numero_execucao = range(
                1,
                len(execucoes) + 1
            )

            plt.plot(
                numero_execucao,
                execucoes,
                marker="o"
            )

            plt.xlabel("Execução")
            plt.ylabel("Tempo (ms)")

            plt.title(
                f"Execuções - {categoria} - "
                f"N = {item['tamanho']:,}"
            )

            plt.grid(
                True,
                linestyle="--",
                alpha=0.5
            )

            plt.tight_layout()

            nome_categoria = (
                categoria
                .replace("Ordem ", "")
                .replace(" ", "_")
                .replace("/", "_")
                .replace("\\", "_")
            )

            caminho = os.path.join(
                PASTA_GRAFICOS,
                f"03_execucoes_{nome_categoria}_N_{item['tamanho']}.png"
            )

            plt.savefig(caminho, dpi=300)
            plt.show()
            plt.close()


# ============================================================
# IMPRIMIR RESUMO DOS DADOS
# ============================================================

def mostrar_resumo(dados):

    print("\n" + "=" * 60)
    print("RESUMO DO BENCHMARK")
    print("=" * 60)

    for categoria, valores in dados.items():

        print(f"\n{categoria}")

        for item in valores:

            print(
                f"  N = {item['tamanho']:,} | "
                f"Média = {item['media']:,.2f} ms | "
                f"Execuções = {len(item['execucoes'])}"
            )


# ============================================================
# PROGRAMA PRINCIPAL
# ============================================================

def main():

    print("=" * 60)
    print("GERADOR DE GRÁFICOS - BUBBLE SORT")
    print("=" * 60)

    # 1. Procurar o arquivo ODS
    caminho_ods = encontrar_ods()

    # 2. Ler os dados
    dados = ler_benchmark(caminho_ods)

    if not dados:
        print("ERRO: Nenhum dado de benchmark foi encontrado.")
        sys.exit(1)

    # 3. Criar pasta de saída
    criar_pasta_graficos()

    # 4. Mostrar dados encontrados
    mostrar_resumo(dados)

    # 5. Gerar gráficos
    print("\nGerando gráficos...\n")

    grafico_comparativo(dados)
    graficos_individuais(dados)
    grafico_barras(dados)
    grafico_execucoes(dados)

    print("\n" + "=" * 60)
    print("CONCLUÍDO!")
    print("=" * 60)

    print(
        f"\nTodos os gráficos foram salvos em:\n"
        f"{PASTA_GRAFICOS}"
    )


if __name__ == "__main__":
    main()
