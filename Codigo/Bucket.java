import java.util.ArrayList;

public class Bucket {
    public void ordenar(Integer[] arr) {
        if (arr.length == 0) {
            return;
        }

        int maior = arr[0];

        for (int i = 1; i < arr.length; i++) {
            if (arr[i] > maior) {
                maior = arr[i];
            }
        }

        ArrayList<Integer>[] baldes = new ArrayList[maior + 1];

        for (int i = 0; i <= maior; i++) {
            baldes[i] = new ArrayList<>();
        }

        for (int i = 0; i < arr.length; i++) {
            baldes[arr[i]].add(arr[i]);
        }

        int indice = 0;

        for (int i = 0; i <= maior; i++) {
            for (int numero : baldes[i]) {
                arr[indice] = numero;
                indice++;
            }
        }
    }
}