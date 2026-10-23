
// Criado por Kevin Meireles e Joao Rigo

import java.util.Random;
import java.util.Scanner;

public class Main {

    public static void main(String[] args) {

        Scanner scan = new Scanner(System.in);
        Random rand = new Random();

        System.out.println("------------------Atividade I------------------");
        System.out.println("Digite o tamanho do vetor para ordenar:");
        System.out.println("-----------------------------------------------");

        int tam = scan.nextInt();

        if (tam <= 0) {
            System.out.println("O tamanho do vetor deve ser maior que zero.");
            scan.close();
            return;
        }

        Integer[] vetor = new Integer[tam];

        System.out.println("-------------Ordem do vetor-------------");
        System.out.println("1) Crescente");
        System.out.println("2) Decrescente");
        System.out.println("3) Aleatória");
        System.out.println("4) Elementos repetidos");
        System.out.println("----------------------------------------");
        System.out.println("Digite a ordem:");

        int ordem = scan.nextInt();

        switch (ordem) {

            case 1:
                for (int i = 0; i < vetor.length; i++) {
                    vetor[i] = i;
                }
                break;

            case 2:
                for (int i = 0; i < vetor.length; i++) {
                    vetor[i] = vetor.length - i;
                }
                break;

            case 3:
                for (int i = 0; i < vetor.length; i++) {
                    vetor[i] = rand.nextInt(100000);
                }
                break;

            case 4:
                int[] valores = {5, 2, 5, 3, 2, 5, 1, 3, 2, 1};

                for (int i = 0; i < vetor.length; i++) {
                    vetor[i] = valores[i % valores.length];
                }
                break;

            default:
                System.out.println("Opção inválida");
                scan.close();
                return;
        }

        int op = -1;

        while (op != 0) {

            System.out.println("----------------Algoritmos-------------------");
            System.out.println("0) Sair");
            System.out.println("1) Merge");
            System.out.println("2) Quick");
            System.out.println("3) Heap");
            System.out.println("4) Counting");
            System.out.println("5) Radix");
            System.out.println("6) Bucket");
            System.out.println("7) Bubble");
            System.out.println("8) Insertion");
            System.out.println("9) Selection");
            System.out.println("10) Shell");
            System.out.println("-----------------------------------------------");
            System.out.println("Digite o Algoritmo para realizar ordenação:");
            System.out.println("-----------------------------------------------");

            op = scan.nextInt();

            if (op == 0) {
                break;
            }

            if (op < 1 || op > 10) {
                System.out.println("Opção inválida!");
                continue;
            }

            // Armazena os tempos das 10 execuções
            double[] tempos = new double[10];

            double soma = 0;
            double maximo = Double.NEGATIVE_INFINITY;
            double minimo = Double.POSITIVE_INFINITY;

            System.out.println();
            System.out.println("========== EXECUTANDO 10 VEZES ==========");

            for (int execucao = 0; execucao < 10; execucao++) {

                Integer[] copia = vetor.clone();

                long inicio = System.nanoTime();

                switch (op) {

                    case 1:
                        Merge merge = new Merge();
                        merge.ordenar(copia);
                        break;

                    case 2:
                        Quick quick = new Quick();
                        quick.ordenar(copia);
                        break;

                    case 3:
                        Heap heap = new Heap();
                        heap.ordenar(copia);
                        break;

                    case 4:
                        Counting counting = new Counting();
                        counting.ordenar(copia);
                        break;

                    case 5:
                        Radix radix = new Radix();
                        radix.ordenar(copia);
                        break;

                    case 6:
                        Bucket bucket = new Bucket();
                        bucket.ordenar(copia);
                        break;

                    case 7:
                        Bubble bubble = new Bubble();
                        bubble.ordenar(copia);
                        break;

                    case 8:
                        Insertion insertion = new Insertion();
                        insertion.ordenar(copia);
                        break;

                    case 9:
                        Selection selection = new Selection();
                        selection.ordenar(copia);
                        break;

                    case 10:
                        Shell shell = new Shell();
                        shell.ordenar(copia);
                        break;
                }

                long fim = System.nanoTime();

                double tempo = (fim - inicio) / 1_000_000.0;

                tempos[execucao] = tempo;
                soma += tempo;

                if (tempo > maximo) {
                    maximo = tempo;
                }

                if (tempo < minimo) {
                    minimo = tempo;
                }

                System.out.printf(
                        "Execução %d: %.3f ms%n",
                        execucao + 1,
                        tempo
                );
            }

            // Calcula a média
            double media = soma / tempos.length;

            // Calcula a soma dos quadrados das diferenças
            double somaQuadrados = 0;

            for (int i = 0; i < tempos.length; i++) {
                double diferenca = tempos[i] - media;
                somaQuadrados += diferenca * diferenca;
            }

            // Desvio padrão populacional das 10 execuções
            double desvioPadrao = Math.sqrt(
                    somaQuadrados / tempos.length
            );

            // Exibe as estatísticas
            System.out.println("-------------------------------------------");
            System.out.printf("MÉDIA:          %.3f ms%n", media);
            System.out.printf("MÁXIMO:         %.3f ms%n", maximo);
            System.out.printf("MÍNIMO:         %.3f ms%n", minimo);
            System.out.printf("DESVIO PADRÃO:  %.3f ms%n", desvioPadrao);
            System.out.println("===========================================");
            System.out.println();
        }

        scan.close();
    }
}
