package hr.fer.zemris.linearna.vjezba1.matrix;

import java.util.Arrays;

public class MatrixSubMatrixView extends AbstractMatrix {

    private int[] rowIndexes;
    private int[] colIndexes;
    private IMatrix matrix;

    public MatrixSubMatrixView(IMatrix matrix, int rowToSkip, int colToSkip) {
        this.matrix = matrix;

        rowIndexes = new int[matrix.getRowsCount() - 1];
        colIndexes = new int[matrix.getColsCount() - 1];

        for (int i = 0; i < rowIndexes.length; i++)
            rowIndexes[i] = i < rowToSkip ? i : i + 1;

        for (int i = 0; i < colIndexes.length; i++)
            colIndexes[i] = i < colToSkip ? i : i + 1;
    }

    private MatrixSubMatrixView(IMatrix matrix, int[] rowsIndexes, int[] colsIndexes) {
        this.matrix = matrix;
        this.rowIndexes = Arrays.copyOf(rowsIndexes, rowsIndexes.length);
        this.colIndexes = Arrays.copyOf(colsIndexes, colsIndexes.length);
    }

    @Override
    public int getRowsCount() {
        return rowIndexes.length;
    }

    @Override
    public int getColsCount() {
        return colIndexes.length;
    }

    @Override
    public double get(int i, int j) {
        return matrix.get(rowIndexes[i], colIndexes[j]);
    }

    @Override
    public IMatrix set(int i, int j, double d) {
        matrix.set(rowIndexes[i], colIndexes[j], d);
        return this;
    }

    @Override
    public IMatrix copy() {
        return new MatrixSubMatrixView(matrix.copy(), rowIndexes, colIndexes);
    }

    @Override
    public IMatrix newInstance(int i, int j) {
        return new Matrix(i, j);
    }
}
