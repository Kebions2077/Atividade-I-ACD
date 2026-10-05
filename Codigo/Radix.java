public class Radix extends Ordenador {

    @Override
    @SuppressWarnings("unchecked")
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        if (arr == null || arr.length == 0) return;

        if (!(arr[0] instanceof Integer)) {
            throw new UnsupportedOperationException("Radix sort so suporta Integer");
        }

        int[] copia = new int[arr.length];
        for (int i = 0; i < arr.length; i++) {
            copia[i] = (Integer) arr[i];
        }

        int maior = copia[0];
        for (int i = 1; i < copia.length; i++) {
            if (copia[i] > maior) maior = copia[i];
        }

        for (int exp = 1; maior / exp > 0; exp *= 10) {
            countingSort(copia, exp);
        }

        for (int i = 0; i < arr.length; i++) {
            arr[i] = (T) Integer.valueOf(copia[i]);
        }
    }

    private void countingSort(int[] arr, int exp) {
        int[] saida = new int[arr.length];
        int[] contagem = new int[10];

        for (int i = 0; i < arr.length; i++) {
            int digito = (arr[i] / exp) % 10;
            contagem[digito]++;
        }

        for (int i = 1; i < 10; i++) {
            contagem[i] += contagem[i - 1];
        }

        for (int i = arr.length - 1; i >= 0; i--) {
            int digito = (arr[i] / exp) % 10;
            saida[contagem[digito] - 1] = arr[i];
            contagem[digito]--;
        }

        for (int i = 0; i < arr.length; i++) {
            arr[i] = saida[i];
        }
    }
}