package hr.fer.zemris.apr.dz1;

import hr.fer.zemris.linearna.vjezba1.matrix.IMatrix;
import hr.fer.zemris.linearna.vjezba1.matrix.Matrix;
import hr.fer.zemris.linearna.vjezba1.matrix.SquareMatrix;

public class Demo {

    public static void main(String[] args) {
        SquareMatrix A = (SquareMatrix) Matrix.parseSimple("2 2 3 | 2 3 0 | 0 4 2");
        // LUP
        int[] P = new int[A.getRowsCount()];
        SquareMatrix LU = A.LUPDecompose(P);
        System.out.println(LU);
        IMatrix b = Matrix.parseSimple("25 | 10 | 10");
        // Ly = bP
        b.switchRows(P);
        b = LU.substituteForwards(b);
        System.out.println(b);
        // Ux = y
        b = LU.substituteBackwards(b);
        System.out.println(b);
    }
}
