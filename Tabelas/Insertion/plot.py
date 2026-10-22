
    for nome in secoes:
        secoes[nome].sort(key=lambda item: item["N"])

    return secoes


def gerar_graficos(secoes):
    if not secoes:
        raise ValueError("Não foram encontrados dados de benchmark na planilha.")

    # Um gráfico de tempo médio por cenário.
    for nome, linhas in secoes.items():
        linhas_validas = [x for x in linhas if pd.notna(x["media"])]
        if not linhas_validas:
            continue

        tamanhos = [x["N"] for x in linhas_validas]
        medias = [x["media"] for x in linhas_validas]

        plt.figure(figsize=(9, 5))
        plt.plot(tamanhos, medias, marker="o", linewidth=2)
        plt.xscale("log")
        plt.yscale("log")
        plt.title(f"Insertion Sort — {nome}")
        plt.xlabel("Tamanho da entrada (N)")
        plt.ylabel("Tempo médio (ms)")
        plt.grid(True, which="both", linestyle="--", alpha=0.35)
        plt.tight_layout()
        destino = PASTA_SAIDA / f"{nome_seguro(nome)}.png"
        plt.savefig(destino, dpi=160)
        plt.close()
        print(f"Gráfico salvo: {destino.name}")

    # Comparação dos cenários no mesmo gráfico.
    plt.figure(figsize=(10, 6))
    for nome, linhas in secoes.items():
        validas = [x for x in linhas if pd.notna(x["media"])]
        if validas:
            plt.plot(
                [x["N"] for x in validas],
                [x["media"] for x in validas],
                marker="o",
                linewidth=2,
                label=nome
            )

    plt.xscale("log")
    plt.yscale("log")
    plt.title("Insertion Sort — comparação dos tipos de entrada")
    plt.xlabel("Tamanho da entrada (N)")
    plt.ylabel("Tempo médio (ms)")
    plt.grid(True, which="both", linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    destino = PASTA_SAIDA / "comparacao_todos_os_tipos.png"
    plt.savefig(destino, dpi=160)
    plt.close()
    print(f"Gráfico salvo: {destino.name}")

    # Boxplots com as execuções individuais para cada tamanho.
    for nome, linhas in secoes.items():
        validas = [x for x in linhas if x["execucoes"]]
        if not validas:
            continue

        dados = [x["execucoes"] for x in validas]
        rotulos = [str(x["N"]) for x in validas]

        plt.figure(figsize=(9, 5))
        plt.boxplot(dados, tick_labels=rotulos)
        plt.yscale("log")
        plt.title(f"Insertion Sort — variação entre execuções: {nome}")
        plt.xlabel("Tamanho da entrada (N)")
        plt.ylabel("Tempo por execução (ms)")
        plt.grid(True, axis="y", which="both", linestyle="--", alpha=0.35)
        plt.tight_layout()
        destino = PASTA_SAIDA / f"{nome_seguro(nome)}_execucoes.png"
        plt.savefig(destino, dpi=160)
        plt.close()
        print(f"Gráfico salvo: {destino.name}")


def main():
    try:
        arquivo = encontrar_arquivo()
        print(f"Arquivo selecionado: {arquivo.name}")
        secoes = ler_dados(arquivo)

        print("\nDados identificados:")
        for nome, linhas in secoes.items():
            tamanhos = [x["N"] for x in linhas]
            print(f"- {nome}: tamanhos {tamanhos}")

        gerar_graficos(secoes)
        print(f"\nConcluído! Gráficos salvos em: {PASTA_SAIDA}")
    except Exception as erro:
        print(f"Erro: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
