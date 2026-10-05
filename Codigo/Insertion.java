public class Insertion extends Ordenador {
    @Override
    public <T extends Comparable<T>> void ordenar(T[] vetor) {
        for (int i = 1; i < vetor.length; i++) {
            T chave = vetor[i];
            int j = i - 1;

            while (j >= 0 && vetor[j].compareTo(chave) > 0) {
                vetor[j + 1] = vetor[j];
                j--;
            }

            vetor[j + 1] = chave;
        }
    }
}