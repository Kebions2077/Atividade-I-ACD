// Criado por Kevin Meireles e Joao Rigo
import java.util.Random;
import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        int tam = 0;
        Scanner scan = new Scanner(System.in);
        Random rand = new Random();

        System.out.println("------------------Atividade I------------------");
        System.out.println("Digite o tamanho do vetor para ordenar:");
        System.out.println("-----------------------------------------------");
        tam = scan.nextInt();

        Integer[] vetor = new Integer[tam];

        System.out.println("-------------Ordem do vetor-------------");
        System.out.println("1) Crescente");
        System.out.println("2) Decrescente");
        System.out.println("3) Aleatória");
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

            default:
                System.out.println("Opção inválida");
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

            double soma = 0;

            System.out.println();
            System.out.println("========== EXECUTANDO 10 VEZES ==========");

            for (int execucao = 1; execucao <= 10; execucao++) {

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

                    default:
                        System.out.println("Opção inválida");
                        execucao = 10;
                        continue;
                }

                long fim = System.nanoTime();

                double tempo = (fim - inicio) / 1_000_000.0;

                soma += tempo;

                System.out.printf(
                        "Execução %d: %.3f ms%n",
                        execucao,
                        tempo
                );
            }

            double media = soma / 10;

            System.out.println("-------------------------------------------");
            System.out.printf("MÉDIA: %.3f ms%n", media);
            System.out.println("===========================================");
            System.out.println();
        }

        scan.close();
    }
}