    return texto or "grafico"


def gerar_graficos(secoes):
    if not secoes:
        raise ValueError(
            "Não foram encontradas seções com dados. Verifique o formato da planilha."
        )

    # 1. Um gráfico de tempo médio para cada tipo de entrada.
    for nome, linhas in secoes.items():
        tamanhos = [linha["N"] for linha in linhas]
        medias = [linha["Media_ms"] for linha in linhas]

        plt.figure(figsize=(9, 5))
        plt.plot(tamanhos, medias, marker="o", linewidth=2)
        plt.xscale("log")
        plt.yscale("log")
        plt.title(f"Counting Sort — {nome}")
        plt.xlabel("Tamanho da entrada (N)")
        plt.ylabel("Tempo médio (ms)")
        plt.grid(True, which="both", linestyle="--", alpha=0.35)
        plt.tight_layout()
        destino = PASTA_SAIDA / f"{nome_seguro(nome)}.png"
        plt.savefig(destino, dpi=160)
        plt.close()
        print(f"Gráfico salvo: {destino.name}")

    # 2. Comparação entre todos os tipos de entrada.
    plt.figure(figsize=(10, 6))
    for nome, linhas in secoes.items():
        tamanhos = [linha["N"] for linha in linhas]
        medias = [linha["Media_ms"] for linha in linhas]
        plt.plot(tamanhos, medias, marker="o", linewidth=2, label=nome)

    plt.xscale("log")
    plt.yscale("log")
    plt.title("Counting Sort — comparação dos tipos de entrada")
    plt.xlabel("Tamanho da entrada (N)")
    plt.ylabel("Tempo médio (ms)")
    plt.grid(True, which="both", linestyle="--", alpha=0.35)
    plt.legend()
    plt.tight_layout()
    destino = PASTA_SAIDA / "comparacao_todos_os_tipos.png"
    plt.savefig(destino, dpi=160)
    plt.close()
    print(f"Gráfico salvo: {destino.name}")

    # 3. Dispersão das execuções (quando há várias medições por tamanho).
    for nome, linhas in secoes.items():
        pontos = [
            (linha["N"], tempo)
            for linha in linhas
            for tempo in linha["Execucoes_ms"]
        ]
        if not pontos:
            continue

        tamanhos = sorted({n for n, _ in pontos})
        valores = [
            [tempo for n, tempo in pontos if n == tamanho]
            for tamanho in tamanhos
        ]

        plt.figure(figsize=(9, 5))
        plt.boxplot(valores, labels=[f"{n:g}" for n in tamanhos])
        plt.yscale("log")
        plt.title(f"Counting Sort — variação entre execuções: {nome}")
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
        arquivo = encontrar_arquivo_ods()
        print(f"Arquivo selecionado: {arquivo.name}")

        secoes = ler_benchmark(arquivo)
        if not secoes:
            raise ValueError("Nenhum dado de benchmark foi reconhecido na planilha.")

        print("\nDados identificados:")
        for nome, linhas in secoes.items():
            print(f"- {nome}: {len(linhas)} tamanhos de entrada")

        gerar_graficos(secoes)
        print(f"\nConcluído! Os gráficos estão em: {PASTA_SAIDA}")

    except Exception as erro:
        print(f"Erro: {erro}")
        sys.exit(1)


if __name__ == "__main__":
    main()
