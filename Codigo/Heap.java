public class Heap extends Ordenador {
    @Override
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        int n = arr.length;

        for (int i = n / 2 - 1; i >= 0; i--) {
            heapify(arr, n, i);
        }

        for (int i = n - 1; i > 0; i--) {
            T temp = arr[0];
            arr[0] = arr[i];
            arr[i] = temp;

            heapify(arr, i, 0);
        }
    }

    private <T extends Comparable<T>> void heapify(T[] arr, int n, int i) {
        int maior = i;
        int esquerda = 2 * i + 1;
        int direita = 2 * i + 2;

        if (esquerda < n && arr[esquerda].compareTo(arr[maior]) > 0) {
            maior = esquerda;
        }

        if (direita < n && arr[direita].compareTo(arr[maior]) > 0) {
            maior = direita;
        }

        if (maior != i) {
            T temp = arr[i];
            arr[i] = arr[maior];
            arr[maior] = temp;

            heapify(arr, n, maior);
        }
    }
}