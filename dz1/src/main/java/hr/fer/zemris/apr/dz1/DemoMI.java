package hr.fer.zemris.apr.dz1;

import hr.fer.zemris.linearna.vjezba1.matrix.Matrix;
import hr.fer.zemris.linearna.vjezba1.matrix.SquareMatrix;

public class DemoMI {

    public static void main(String[] args) {
        SquareMatrix A = (SquareMatrix) Matrix.parseSimple("1 2 3 4 | 3 2 1 4 | 1 3 2 4 | 1 4 2 3");
        int[] index = new int[4];
        SquareMatrix LUP = A.LUPDecompose(index);
        System.out.println(LUP);
        System.out.println(formatArray(index));
    }

    private static String formatArray(int[] arr) {
        StringBuilder sb = new StringBuilder();
        sb.append('[');
        for (int element : arr)
            sb.append(element).append(',').append(' ');

        sb.append(']');
        return sb.toString();
    }

}
