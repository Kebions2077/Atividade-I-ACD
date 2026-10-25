
import java.io.*;
import java.nio.charset.StandardCharsets;
import java.nio.file.*;
import java.util.*;

public class Main {
    static final int EXECUCOES = 10;
    static final String[] NOMES = {
            "", "Merge", "Quick", "Heap", "Counting", "Radix",
            "Bucket", "Bubble", "Insertion", "Selection", "Shell"
    };
    static final String[] ORDENS = {
            "", "Crescente", "Decrescente", "Aleatoria", "Repetidos"
    };

    static class Resultado {
        String algoritmo, ordem;
        int n;
        double[] tempos;
        double media, maximo, minimo, desvio;

        Resultado(String algoritmo, int n, String ordem, double[] tempos) {
            this.algoritmo = algoritmo;
            this.n = n;
            this.ordem = ordem;
            this.tempos = tempos;

            double soma = 0;
            minimo = Double.POSITIVE_INFINITY;
            maximo = Double.NEGATIVE_INFINITY;

            for (double t : tempos) {
                soma += t;
                minimo = Math.min(minimo, t);
                maximo = Math.max(maximo, t);
            }

            media = soma / tempos.length;
            double sq = 0;

            for (double t : tempos)
                sq += Math.pow(t - media, 2);

            desvio = Math.sqrt(sq / tempos.length);
        }

        void mostrar() {
            System.out.printf(Locale.US,
                    "N=%d | %s | Media=%.3f ms | Max=%.3f ms | Min=%.3f ms | DP=%.3f ms%n",
                    n, ordem, media, maximo, minimo, desvio);
        }
    }

    public static void main(String[] args) {
        Scanner sc = new Scanner(System.in);
        Random rand = new Random();

        System.out.println("1) Manual");
        System.out.println("2) Automatico - todos os algoritmos");
        System.out.println("3) Testes com vetores pequenos");
        System.out.println("0) Sair");

        int modo = ler(sc);

        if (modo == 1) {
            System.out.print("Tamanho N: ");
            int n = ler(sc);

            System.out.println(
                    "1) Crescente  2) Decrescente  3) Aleatoria  4) Repetidos");
            int ordem = ler(sc);

            if (n <= 0 || ordem < 1 || ordem > 4) {
                System.out.println("Entrada invalida.");
            } else {
                Integer[] vetor = criarVetor(n, ordem, rand);

                while (true) {
                    for (int i = 1; i <= 10; i++)
                        System.out.println(i + ") " + NOMES[i]);

                    System.out.println("0) Sair");
                    int op = ler(sc);

                    if (op == 0) break;
                    if (op < 1 || op > 10) continue;

                    executar(op, vetor, ordem);
                }
            }

        } else if (modo == 2) {
            List<Resultado> resultados = new ArrayList<>();

            for (int op = 1; op <= 10; op++) {
                System.out.println("\n=== " + NOMES[op] + " ===");
                automatico(op, rand, resultados);
            }

            try {
                exportar(resultados);
                System.out.println(
                        "\nRelatorios e graficos salvos na pasta resultados.");
            } catch (Exception e) {
                System.err.println(
                        "Erro ao gerar relatorios: " + e.getMessage());
            }

        } else if (modo == 3) {
            testarAlgoritmos();

        } else if (modo != 0) {
            System.out.println("Opcao invalida.");
        }

        sc.close();
    }

    static int ler(Scanner sc) {
        while (!sc.hasNextInt()) {
            System.out.print("Digite um numero inteiro: ");
            sc.next();
        }
        return sc.nextInt();
    }

    static Integer[] criarVetor(int n, int ordem, Random r) {
        Integer[] v = new Integer[n];
        int[] repetidos = {5, 2, 5, 3, 2, 5, 1, 3, 2, 1};

        for (int i = 0; i < n; i++) {
            switch (ordem) {
                case 1: v[i] = i; break;
                case 2: v[i] = n - i; break;
                case 3: v[i] = r.nextInt(100000); break;
                case 4: v[i] = repetidos[i % repetidos.length]; break;
            }
        }

        return v;
    }

    static void ordenar(int op, Integer[] v) {
        switch (op) {
            case 1: new Merge().ordenar(v); break;
            case 2: new Quick().ordenar(v); break;
            case 3: new Heap().ordenar(v); break;
            case 4: new Counting().ordenar(v); break;
            case 5: new Radix().ordenar(v); break;
            case 6: new Bucket().ordenar(v); break;
            case 7: new Bubble().ordenar(v); break;
            case 8: new Insertion().ordenar(v); break;
            case 9: new Selection().ordenar(v); break;
            case 10: new Shell().ordenar(v); break;
            default: throw new IllegalArgumentException("Algoritmo invalido");
        }
    }

    static Resultado executar(int op, Integer[] vetor, int ordem) {
        double[] tempos = new double[EXECUCOES];

        for (int i = 0; i < EXECUCOES; i++) {
            Integer[] copia = vetor.clone();
            long inicio = System.nanoTime();

            ordenar(op, copia);

            tempos[i] = (System.nanoTime() - inicio) / 1_000_000.0;
            System.out.printf(Locale.US,
                    "Execucao %d: %.3f ms%n", i + 1, tempos[i]);
        }

        Resultado r = new Resultado(
                NOMES[op], vetor.length, ORDENS[ordem], tempos);
        r.mostrar();

        return r;
    }

    static void automatico(int op, Random rand,
                           List<Resultado> resultados) {
        int[] tamanhos = (op == 7 || op == 8 || op == 9)
                ? new int[]{1000, 10000, 100000}
                : new int[]{1000, 10000, 100000, 1000000};

        for (int ordem = 1; ordem <= 4; ordem++) {
            for (int n : tamanhos) {
                System.out.printf("%n%s | N=%d | %s%n",
                        NOMES[op], n, ORDENS[ordem]);

                try {
                    resultados.add(executar(
                            op, criarVetor(n, ordem, rand), ordem));
                } catch (Exception e) {
                    System.err.println("Falha: " + e.getMessage());
                }
            }
        }
    }

    // NOVA OPCAO: TESTES COM VETORES PEQUENOS
    static void testarAlgoritmos() {
        Integer[][] vetores = {
                {1, 2, 3, 4, 5, 6, 7, 8, 9, 10},
                {10, 9, 8, 7, 6, 5, 4, 3, 2, 1},
                {5, 2, 9, 1, 7, 3, 8, 4, 6, 0},
                {4, 2, 4, 1, 2, 5, 1, 3, 5, 3},
                {12, -3, 7, 0, -8, 12, 4, 1, 9, -1, 6, 2},
                {15, 0, 15, -5, 8, 3, 3, 11, -2, 7, 1, 9, 4, 6, 2}
        };

        String[] nomes = {
                "Crescente",
                "Decrescente",
                "Aleatorio",
                "Repetidos",
                "Valores negativos",
                "Vetor com 15 elementos"
        };

        int passouTotal = 0;
        int falhouTotal = 0;

        System.out.println("\n===== TESTES DE ORDENACAO =====");

        for (int op = 1; op <= 10; op++) {
            System.out.println("\n=== " + NOMES[op] + " ===");

            for (int i = 0; i < vetores.length; i++) {
                Integer[] original = vetores[i].clone();
                Integer[] esperado = vetores[i].clone();
                Integer[] copia = vetores[i].clone();

                Arrays.sort(esperado);

                try {
                    ordenar(op, copia);

                    boolean passou = Arrays.equals(copia, esperado);

                    System.out.println("\nTeste: " + nomes[i]);
                    System.out.println(
                            "Original: " + Arrays.toString(original));
                    System.out.println(
                            "Ordenado: " + Arrays.toString(copia));

                    if (passou) {
                        System.out.println("Resultado: PASSOU");
                        passouTotal++;
                    } else {
                        System.out.println("Resultado: FALHOU");
                        System.out.println(
                                "Esperado: " + Arrays.toString(esperado));
                        falhouTotal++;
                    }

                } catch (Exception e) {
                    System.out.println("\nTeste: " + nomes[i]);
                    System.out.println(
                            "Resultado: FALHOU - " + e.getMessage());
                    falhouTotal++;
                }
            }
        }

        System.out.println("\n===== RESUMO DOS TESTES =====");
        System.out.println("Total: " + (passouTotal + falhouTotal));
        System.out.println("Passaram: " + passouTotal);
        System.out.println("Falharam: " + falhouTotal);
    }

    static void exportar(List<Resultado> rs) throws Exception {
        Path pasta = Paths.get("resultados").toAbsolutePath();
        Files.createDirectories(pasta.resolve("graficos"));

        StringBuilder csv = new StringBuilder(
                "algoritmo,N,ordem,execucao,tempo_ms,media_ms,maximo_ms,minimo_ms,desvio_padrao_ms\n");

        for (Resultado r : rs) {
            for (int i = 0; i < r.tempos.length; i++) {
                csv.append(String.format(Locale.US,
                        "%s,%d,%s,%d,%.6f,%.6f,%.6f,%.6f,%.6f%n",
                        r.algoritmo, r.n, r.ordem, i + 1, r.tempos[i],
                        r.media, r.maximo, r.minimo, r.desvio));
            }
        }

        Files.write(
                pasta.resolve("dados_benchmark.csv"),
                csv.toString().getBytes(StandardCharsets.UTF_8));

        String py = String.join("\n",
                "from pathlib import Path",
                "import pandas as pd",
                "import matplotlib",
                "matplotlib.use('Agg')",
                "import matplotlib.pyplot as plt",
                "p=Path(__file__).resolve().parent",
                "g=p/'graficos'",
                "d=pd.read_csv(p/'dados_benchmark.csv')",
                "for a,x in d.groupby('algoritmo',sort=False):",
                " x.to_excel(p/f'{a}.ods',index=False,engine='odf')",
                " m=x.groupby(['N','ordem'],as_index=False).tempo_ms.mean()",
                " for ord in ['Crescente','Decrescente','Aleatoria','Repetidos']:",
                "  z=m[m.ordem==ord].sort_values('N')",
                "  if not z.empty: plt.plot(z.N,z.tempo_ms,marker='o',label=ord)",
                " plt.title(f'Tempo de execucao - {a}')",
                " plt.xlabel('Tamanho da entrada (N)')",
                " plt.ylabel('Tempo medio (ms)')",
                " plt.xscale('log')",
                " plt.xticks(sorted(x.N.unique()),[f'{int(n):,}'.replace(',','.') for n in sorted(x.N.unique())])",
                " plt.grid(True,alpha=.3); plt.legend(); plt.tight_layout()",
                " plt.savefig(g/f'{a}.png',dpi=150); plt.close()",
                "r=d.groupby(['algoritmo','N','ordem'],as_index=False).agg(media_ms=('tempo_ms','mean'),maximo_ms=('tempo_ms','max'),minimo_ms=('tempo_ms','min'),desvio_padrao_ms=('tempo_ms','std'))",
                "r.to_excel(p/'Resumo_Geral.ods',index=False,engine='odf')",
                "print('Relatorios gerados.')"
        );

        Path script = pasta.resolve("gerar_relatorios.py");
        Files.write(script, py.getBytes(StandardCharsets.UTF_8));

        String cmd = System.getProperty("os.name")
                .toLowerCase().contains("win") ? "python" : "python3";

        Process processo = new ProcessBuilder(cmd, script.toString())
                .directory(pasta.toFile())
                .redirectErrorStream(true)
                .start();

        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(
                        processo.getInputStream(), StandardCharsets.UTF_8))) {
            String linha;
            while ((linha = br.readLine()) != null)
                System.out.println(linha);
        }

        if (processo.waitFor() != 0)
            throw new IOException(
                    "Instale: pip install pandas odfpy matplotlib");
    }
}
