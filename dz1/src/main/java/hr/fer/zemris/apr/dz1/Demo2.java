package hr.fer.zemris.apr.dz1;

import hr.fer.zemris.linearna.vjezba1.matrix.IMatrix;
import hr.fer.zemris.linearna.vjezba1.matrix.Matrix;
import hr.fer.zemris.linearna.vjezba1.matrix.SquareMatrix;

import java.io.IOException;
import java.nio.file.Path;
import java.nio.file.Paths;

public class Demo2 {

    public static void main(String[] args) throws IOException {
        SquareMatrix A = (SquareMatrix) Matrix.parseSimple("3 2 1 | 1 2 2 | 4 3 4");
        IMatrix b = Matrix.parseSimple("4 | 3 | 8");
        int[] P = new int[]{0, 1, 2};
        // PLU = bP
        SquareMatrix LU = A.LUPDecompose(P);
        System.out.println(P);
        //SquareMatrix LU  = (SquareMatrix) PLU.switchRows(P);
        System.out.println(LU);
        b = b.switchRows(P);
        System.out.println(b);

        IMatrix y = LU.substituteForwards(b);
        System.out.println(LU);

        IMatrix x = LU.substituteBackwards(y);
        System.out.println(x);

        Path p = Paths.get("src/main/resources/4x4zaLUP.txt");
        A = (SquareMatrix) Matrix.fromFile(p);
        System.out.println(A.LUPDecompose(new int[4]));


    }

}

