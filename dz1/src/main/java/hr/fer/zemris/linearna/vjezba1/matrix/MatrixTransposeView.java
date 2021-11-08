package hr.fer.zemris.linearna.vjezba1.matrix;

public class MatrixTransposeView extends AbstractMatrix {

    private IMatrix matrix;

    public MatrixTransposeView(IMatrix matrix) {
        this.matrix = matrix;
    }

    @Override
    public int getRowsCount() {
        return matrix.getColsCount();
    }

    @Override
    public int getColsCount() {
        return matrix.getRowsCount();
    }

    @Override
    public double get(int i, int j) {
        return matrix.get(j, i);
    }

    @Override
    public IMatrix set(int i, int j, double d) {
        return matrix.set(j, i, d);
    }

    @Override
    public IMatrix copy() {
        return new MatrixTransposeView(matrix.copy());
    }

    @Override
    public IMatrix newInstance(int i, int j) {
        return new Matrix(i, j);
    }
}
