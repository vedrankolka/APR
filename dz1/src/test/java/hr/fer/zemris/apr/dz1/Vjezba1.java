package hr.fer.zemris.apr.dz1;

import hr.fer.zemris.linearna.vjezba1.matrix.IMatrix;
import hr.fer.zemris.linearna.vjezba1.matrix.Matrix;
import hr.fer.zemris.linearna.vjezba1.matrix.SquareMatrix;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

import java.io.IOException;
import java.nio.file.Paths;

public class Vjezba1 {

    public static final String DIR = "src/test/resources/";

    @Test
    public void zad2() throws IOException {
        System.out.println("Zadatak 2");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad2_3x3"));
        IMatrix b = Matrix.fromFile(Paths.get(DIR + "zad2_3x1"));

        IMatrix x1 = A.solveForX(b, false, false);
        IMatrix x2 = A.solveForX(b, false, true);

        System.out.println("x1:\n" + x1);
        System.out.println("x2:\n" + x2);
    }

    @Test
    public void zad3() throws IOException {
        System.out.println("Zadatak 3");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad3_3x3"));

        System.out.println("LU:\n" + A.LUDecompose());
        System.out.println("LUP:\n" + A.LUPDecompose(null));

        IMatrix b = Matrix.parseSimple("1 | 2 | 3");

        System.out.println(A.solveForX(b));
    }

    @Test
    public void zad4() throws IOException {
        System.out.println("Zadatak 4");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad4_3x3"));
        IMatrix b = Matrix.fromFile(Paths.get(DIR + "zad4_3x1"));

        System.out.println(A.solveForX(b, false, false));
        System.out.println(A.solveForX(b, false, true));
    }

    @Test
    public void zad5() throws IOException {
        System.out.println("Zadatak 5");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad5_3x3"));
        IMatrix b = Matrix.fromFile(Paths.get(DIR + "zad5_3x1"));
        // x = [0 | 0 | 3] it good
        System.out.println(A.solveForX(b));
    }

    @Test
    public void zad6() throws IOException {
        System.out.println("Zadatak 6");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad6_3x3"));
        IMatrix b = Matrix.fromFile(Paths.get(DIR + "zad6_3x1"));

        System.out.println(A.solveForX(b));
    }

    @Test
    public void zad7() throws IOException {
        System.out.println("Zadatak 7");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad7_3x3"));
        SquareMatrix Ainverted = A.invert();

        Assertions.assertNull(Ainverted);
    }

    @Test
    public void zad8() throws IOException {
        System.out.println("Zadatak 8");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad8_3x3"));
        SquareMatrix Ainverted = A.invert();
        System.out.println("A:\n" + A);
        System.out.println("A^-1\n" + Ainverted);
        System.out.println("A*A^-1\n" + A.nMultiply(Ainverted));
    }

    @Test
    public void zad9() throws IOException {
        System.out.println("Zadatak 9");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad8_3x3"));
        System.out.println("det(A) = " + A.determinant());
    }

    @Test
    public void zad10() throws IOException {
        System.out.println("Zadatak 10");
        SquareMatrix A = (SquareMatrix) Matrix.fromFile(Paths.get(DIR + "zad10_3x3"));
        System.out.println("det(A) = " + A.determinant());
    }
}
