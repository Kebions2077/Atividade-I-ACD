public class Selection extends Ordenador {
    @Override
    public <T extends Comparable<T>> void ordenar(T[] vetor) {

        for (int i = 0; i < vetor.length - 1; i++) {
            int menor = i;

            for (int j = i + 1; j < vetor.length; j++) {
                if (vetor[j].compareTo(vetor[menor]) < 0) {
                    menor = j;
                }
            }

            T temp = vetor[menor];
            vetor[menor] = vetor[i];
            vetor[i] = temp;
        }
    }
}