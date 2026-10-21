public class Quick extends Ordenador {

    @Override
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private <T extends Comparable<T>> void quickSort(T[] arr, int inicio, int fim) {
        while (inicio < fim) {
            T pivo = arr[fim];

            int menor = inicio;
            int atual = inicio;
            int maior = fim;

            while (atual <= maior) {
                int comparacao = arr[atual].compareTo(pivo);

                if (comparacao < 0) {
                    trocar(arr, menor, atual);
                    menor++;
                    atual++;
                } else if (comparacao > 0) {
                    trocar(arr, atual, maior);
                    maior--;
                } else {
                    atual++;
                }
            }

            if (menor - inicio < fim - maior) {
                quickSort(arr, inicio, menor - 1);
                inicio = maior + 1;
            } else {
                quickSort(arr, maior + 1, fim);
                fim = menor - 1;
            }
        }
    }

    private <T extends Comparable<T>> void trocar(T[] arr, int i, int j) {
        T temp = arr[i];
        arr[i] = arr[j];
        arr[j] = temp;
    }
}