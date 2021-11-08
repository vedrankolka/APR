package hr.fer.zemris.linearna.vjezba1.matrix;

import hr.fer.zemris.linearna.vjezba1.IncompatableOperationException;

public class SquareMatrix extends Matrix {

    public SquareMatrix(int rows) {
        super(rows, rows);
    }

    public SquareMatrix(int rows, double[][] elements, boolean live) {
        super(rows, rows, checkIfSquare(elements), live);
    }

    @Override
    public IMatrix copy() {
        return new SquareMatrix(rows, elements, false);
    }

    private static double[][] checkIfSquare(double[][] data) {
        if (data.length != data[0].length)
            throw new IllegalArgumentException("no squerr.");

        return data;
    }

    public IMatrix substituteForwards(IMatrix b) {
        b = b.copy();
        int n = getRowsCount();

        for (int i = 0; i < n - 1; ++i) {
            for (int j = i + 1; j < n; ++j) {
                double d = b.get(j, 0) - this.get(j, i) * b.get(i, 0);
                b.set(j, 0, d);
            }
        }

        return b;
    }

    public IMatrix substituteBackwards(IMatrix b) {
        b = b.copy();
        int n = getRowsCount();

        for (int i = n - 1; i >= 0; i--) {
            b.set(i, 0, b.get(i, 0) / this.get(i, i));
            for (int j = 0; j < i; j++) {
                double d = b.get(j, 0) - this.get(j, i) * b.get(i, 0);
                b.set(j, 0, d);
            }
        }

        return b;
    }

    public SquareMatrix LUDecompose() {
        SquareMatrix A = (SquareMatrix) this.copy();
        int n = getRowsCount();

        for (int i = 0; i < n - 1; i++) {
            for (int j = i + 1; j < n; j++) {
                // check if A[i, i] == 0
                if (Math.abs(A.get(i, i)) < EPSILON) {
                    System.out.println("Na dijagonali je 0.");
                    return null;
                }
                A.set(j, i, A.get(j, i) / A.get(i, i));
                for (int k = i + 1; k < n; k++) {
                    A.set(j, k, A.get(j, k) - A.get(j, i) * A.get(i, k));
                }
            }
        }

        return A;
    }


    public SquareMatrix LUPDecompose(int[] P) {
        int n = getRowsCount();
        SquareMatrix A = (SquareMatrix) this.copy();

        if (P == null) P = A.initRowIndex();
        else for (int i = 0; i < n; i++) P[i] = i;

        for (int i = 0; i < n - 1; i++) {
            int pivot = i;
            for (int j = i + 1; j < n; j++) {
                if (Math.abs(A.get(j, i)) > Math.abs(A.get(pivot, i))) pivot = j;
            }
            swap(P, i, pivot);
            A.switchRows(i, pivot);
            // check if A[i, i] == 0
            if (Math.abs(A.get(i, i)) < EPSILON) {
                System.out.println("Na dijagonali je 0.");
                return null;
            }
            for (int j = i + 1; j < n; j++) {
                A.set(j, i, A.get(j, i) / A.get(i, i));
                for (int k = i + 1; k < n; k++) {
                    double d = A.get(j, k) - A.get(j, i) * A.get(i, k);
                    A.set(j, k, d);
                }
            }
        }

        return A;
    }


    public SquareMatrix invert() {
        int n = getRowsCount();
        int[] rowIndex = initRowIndex();
        SquareMatrix LU = this.LUPDecompose(rowIndex);

        // now solve n times for x with each row of E as b
        SquareMatrix AInverted = new SquareMatrix(n);

        for (int i = 0; i < n; i++) {
            // LUxi = ei
            IMatrix ei = Matrix.e(n, i);
            IMatrix xi = LU.solveForX(ei, true, true);
            if (xi == null) return null;
            // now copy the result into the result matrix
            for (int j = 0; j < n; j++)
                // can't forget to switch columns!
                AInverted.set(j, rowIndex[i], xi.get(j, 0));
        }

        return AInverted;
    }

    public IMatrix solveForX(IMatrix b) {
        return solveForX(b, false, true);
    }

    public IMatrix solveForX(IMatrix b, boolean decomposed, boolean LUP) {

        int n = this.getRowsCount();

        if (b.getColsCount() != 1 && b.getRowsCount() == n)
            throw new IncompatableOperationException("The given matrix b must be a sinlge column matrix with " + n + " rows.");

        SquareMatrix LU;
        if (!decomposed) {
            int[] rowIndex = initRowIndex();
            LU = LUP ? this.LUPDecompose(rowIndex) : this.LUDecompose();
            b.switchRows(rowIndex);
        } else {
            LU = this;
        }
        // check if the matrix can be decomposed
        if (LU == null) return null;
        // check if it is singular
        double det = 1;
        for (int i = 0; i < n; i++) det *= LU.get(i, i);
        if (det == 0) return null;

        IMatrix y = LU.substituteForwards(b);
        IMatrix x = LU.substituteBackwards(y);

        return x;
    }

    public double determinant() {
        int n = getRowsCount();
        int[] rowIndex = initRowIndex();
        SquareMatrix LU = this.LUPDecompose(rowIndex);

        int counter = 0;
        for (int i = 0; i < n; i++) {
            if (rowIndex[i] == i) continue;

            swap(rowIndex, i, rowIndex[i]);
            counter++;
        }

        double sign = counter % 2 == 0 ? 1 : -1;

        double det = 1.0;
        for (int i = 0; i < n; i++)
            det *= LU.get(i, i);

        return sign * det;
    }

    private static void swap(int[] arr, int index1, int index2) {
        int temp = arr[index1];
        arr[index1] = arr[index2];
        arr[index2] = temp;
    }

    public static SquareMatrix E(int n) {
        double[][] data = new double[n][n];

        for (int i = 0; i < n; i++)
            data[i][i] = 1;

        return new SquareMatrix(n, data, true);
    }
}
