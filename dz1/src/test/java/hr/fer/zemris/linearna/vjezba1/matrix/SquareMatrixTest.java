package hr.fer.zemris.linearna.vjezba1.matrix;

import org.junit.jupiter.api.Test;

import static hr.fer.zemris.linearna.vjezba1.matrix.AbstractMatrix.EPSILON;
import static org.junit.jupiter.api.Assertions.*;

public class SquareMatrixTest {

    @Test
    public void solveForXNormalTest() {
        SquareMatrix A = (SquareMatrix) Matrix.parseSimple("3 2 1 | 1 2 2 | 4 3 4");
        IMatrix b = Matrix.parseSimple("4 | 3 | 8");
        IMatrix expectedResult = Matrix.parseSimple("1 | 0 | 1");
        IMatrix calculatedResult = A.solveForX(b, false, true);

        assertEquals(expectedResult, calculatedResult);
    }

    @Test
    public void invertNormalTest() {
        SquareMatrix A = (SquareMatrix) Matrix.parseSimple("2 3 2 | 4 1 1 | 3 2 1");
        SquareMatrix expected = (SquareMatrix) Matrix.parseSimple("-0.2 0.2 0.2 | -0.2 -0.8 1.2 | 1 1 -2");
        SquareMatrix calculated = A.invert();

        assertEquals(expected, calculated);

        A = (SquareMatrix) Matrix.parseSimple("1 0 0 1 | 0 2 1 2 | 2 1 0 1 | 2 0 1 4");
        expected = (SquareMatrix) Matrix.parseSimple("-2 -0.5 1 0.5 | 1 0.5 0 -0.5 | -8 -1 2 2 | 3 0.5 -1 -0.5");
        calculated = A.invert();

        assertEquals(expected, calculated);

        SquareMatrix E = SquareMatrix.E(A.getRowsCount());
        assertEquals(E, A.nMultiply(calculated));
    }

    @Test
    public void determinantNormalTest() {
        SquareMatrix A = (SquareMatrix) Matrix.parseSimple("1 2 | 2 1");
        assertEquals(-3.0, A.determinant(), EPSILON);

        A = (SquareMatrix) Matrix.parseSimple("2 4 1 | 4 1 1 | 2 3 1");
        assertEquals(-2.0, A.determinant(), EPSILON);

        A = (SquareMatrix) Matrix.parseSimple("2 1 2 3 | -1 3 1 0 | 3 2 -2 1 | 4 1 2 1");
        assertEquals(132, A.determinant(), EPSILON);
    }

}
