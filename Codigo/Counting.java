public class Counting extends Ordenador {

    @Override
    @SuppressWarnings("unchecked")
    public <T extends Comparable<T>> void ordenar(T[] arr) {
        if (arr == null || arr.length == 0) return;

        if (!(arr[0] instanceof Integer)) {
            throw new UnsupportedOperationException("Counting sort so suporta Integer");
        }

        int maior = (Integer) arr[0];
        for (T v : arr) {
            int x = (Integer) v;
            if (x > maior) maior = x;
        }

        int[] contagem = new int[maior + 1];
        for (T v : arr) {
            contagem[(Integer) v]++;
        }

        int indice = 0;
        for (int i = 0; i < contagem.length; i++) {
            while (contagem[i]-- > 0) {
                arr[indice++] = (T) Integer.valueOf(i);
            }
        }
    }
}