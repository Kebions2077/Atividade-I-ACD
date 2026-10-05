public class Shell extends Ordenador {
    @Override
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        int n = arr.length;

        for (int gap = n / 2; gap > 0; gap /= 2) {

            for (int i = gap; i < n; i++) {
                T temp = arr[i];
                int j;

                for (j = i; j >= gap && arr[j - gap].compareTo(temp) > 0; j -= gap) {
                    arr[j] = arr[j - gap];
                }

                arr[j] = temp;
            }
        }
    }
}