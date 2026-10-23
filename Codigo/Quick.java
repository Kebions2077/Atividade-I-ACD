
public class Quick extends Ordenador {

    @Override
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        if (arr == null || arr.length < 2) {
            return;
        }

        quickSort(arr, 0, arr.length - 1);
    }

    private <T extends Comparable<T>> void quickSort(
            T[] arr, int inicio, int fim) {

        while (inicio < fim) {

            // Mediana de três: primeiro, meio e último
            int meio = inicio + (fim - inicio) / 2;

            if (arr[inicio].compareTo(arr[meio]) > 0) {
                trocar(arr, inicio, meio);
            }

            if (arr[inicio].compareTo(arr[fim]) > 0) {
                trocar(arr, inicio, fim);
            }

            if (arr[meio].compareTo(arr[fim]) > 0) {
                trocar(arr, meio, fim);
            }

            T pivo = arr[meio];

            int menor = inicio;
            int atual = inicio;
            int maior = fim;

            // Particionamento em três caminhos
            while (atual <= maior) {

                int comparacao = arr[atual].compareTo(pivo);

                if (comparacao < 0) {

                    if (menor != atual) {
                        trocar(arr, menor, atual);
                    }

                    menor++;
                    atual++;

                } else if (comparacao > 0) {

                    if (atual != maior) {
                        trocar(arr, atual, maior);
                    }

                    maior--;

                } else {
                    atual++;
                }
            }

            // Recursão na menor partição
            // e processamento iterativo da maior
            int tamanhoEsquerda = menor - inicio;
            int tamanhoDireita = fim - maior;

            if (tamanhoEsquerda < tamanhoDireita) {

                if (inicio < menor - 1) {
                    quickSort(arr, inicio, menor - 1);
                }

                inicio = maior + 1;

            } else {

                if (maior + 1 < fim) {
                    quickSort(arr, maior + 1, fim);
                }

                fim = menor - 1;
            }
        }
    }

    private <T extends Comparable<T>> void trocar(
            T[] arr, int i, int j) {

        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}
