public class Quick extends Ordenador {
    @Override
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        quickSort(arr, 0, arr.length - 1);
    }

    private <T extends Comparable<T>> void quickSort(T[] arr, int inicio, int fim) {
        if (inicio < fim) {
            int pivo = particionar(arr, inicio, fim);

            quickSort(arr, inicio, pivo - 1);
            quickSort(arr, pivo + 1, fim);
        }
    }

    private <T extends Comparable<T>> int particionar(T[] arr, int inicio, int fim) {
        T pivo = arr[fim];
        int i = inicio - 1;

        for (int j = inicio; j < fim; j++) {
            if (arr[j].compareTo(pivo) <= 0) {
                i++;

                T temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }
        }

        T temp = arr[i + 1];
        arr[i + 1] = arr[fim];
        arr[fim] = temp;

        return i + 1;
    }
}