package hr.fer.zemris.linearna.vjezba1.matrix;

import hr.fer.zemris.linearna.vjezba1.IncompatableOperationException;
import hr.fer.zemris.linearna.vjezba1.vector.IVector;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.Arrays;

public abstract class AbstractMatrix implements IMatrix {

    public static final double EPSILON = 10e-12;

    @Override
    public IMatrix nTranspose(boolean live) {
        if (live) {
            return new MatrixTransposeView(this);
        } else {
            IMatrix transposed = newInstance(getColsCount(), getRowsCount());
            for (int i = 0; i < getRowsCount(); i++) {
                for (int j = 0; j < getColsCount(); j++) {
                    transposed.set(j, i, get(i, j));
                }
            }

            return transposed;
        }
    }

    @Override
    public IMatrix add(IMatrix m) {

        for (int i = 0; i < getRowsCount(); i++)
            for (int j = 0; j < getColsCount(); j++)
                set(i, j, get(i, j) + m.get(i, j));

        return this;
    }

    @Override
    public IMatrix nAdd(IMatrix m) {
        return copy().add(m);
    }

    @Override
    public IMatrix sub(IMatrix m) {

        for (int i = 0; i < getRowsCount(); i++)
            for (int j = 0; j < getColsCount(); j++)
                set(i, j, get(i, j) - m.get(i, j));

        return this;
    }

    @Override
    public IMatrix nSub(IMatrix m) {
        return copy().sub(m);
    }

    @Override
    public IMatrix nMultiply(IMatrix matrix) {
        checkDimensions(matrix);
        int n = this.getRowsCount();
        int m = matrix.getColsCount();
        IMatrix result = newInstance(n, m);

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) {
                double sum = 0.0;
                for (int k = 0; k < this.getColsCount(); k++)
                    sum += this.get(i, k) * matrix.get(k, j);
                result.set(i, j, sum);
            }
        }

        return result;
    }

    @Override
    public double determinant() {
        if (getRowsCount() != getColsCount())
            throw new IncompatableOperationException("A matrix must be square to have a determinant.");

        if (getRowsCount() == 1)
            return get(0, 0);

        double sum = 0.0;
        double s = 1;

        for (int j = 0; j < getColsCount(); j++) {
            IMatrix subMatrix = new MatrixSubMatrixView(this, 0, j);
            sum += get(0, j) * s * subMatrix.determinant();
            s *= -1;
        }

        return sum;
    }

    @Override
    public IMatrix subMatrix(int i, int j, boolean live) {
        if (live) {
            return new MatrixSubMatrixView(this, i, j);
        } else {
            int n = getRowsCount() - 1;
            int m = getColsCount() - 1;
            double[][] data = new double[n][m];
            for (int k = 0; k < n; k++) {
                int rowIndex = k < i ? k : k + 1;
                for (int l = 0; l < m; l++) {
                    int colIndex = l < j ? l : l + 1;
                    data[k][j] = get(rowIndex, colIndex);
                }
            }

            return new Matrix(n, m, data, false);
        }
    }

    @Override
    public IMatrix nInvert() {
        double determinant = determinant();
        if (determinant == 0)
            throw new IncompatableOperationException("This matrix is singular.");

        return null;
    }

    @Override
    public double[][] toArray() {
        int n = getRowsCount();
        int m = getColsCount();
        double[][] data = new double[n][m];

        for (int i = 0; i < n; i++)
            for (int j = 0; j < m; j++)
                data[i][j] = get(i, j);

        return data;
    }

    @Override
    public IVector toVector(boolean b) {
        // TODO
        return null;
    }

//    @Override
//    public IMatrix switchRows(int[] index) {
//        index = Arrays.copyOf(index, index.length);
//        IMatrix temp = this.copy();
//        for (int i = 0; i < index.length; i++) {
//            if (index[i] == i)
//                continue;
//
//            // switch the rows in the matrix
//            switchRows(i, index[i]);
//            // then also record the switch in the index
//            int temp = index[index[i]];
//            index[index[i]] = index[i];
//            index[i] = temp;

//        }
//
//        return this;
//    }


    @Override
    public IMatrix switchRows(int[] index) {
        IMatrix temp = this.copy();
        for (int i = 0; i < index.length; i++) {
            for (int k = 0; k < getColsCount(); k++) temp.set(i, k, this.get(index[i], k));
        }

        return copyToSelf(temp);
    }

    public IMatrix copyToSelf(IMatrix toCopy) {
        int n = Math.min(this.getRowsCount(), toCopy.getRowsCount());
        int m = Math.min(this.getColsCount(), toCopy.getColsCount());

        for (int i = 0; i < n; i++) {
            for (int j = 0; j < m; j++) this.set(i, j, toCopy.get(i, j));
        }

        return this;
    }

    @Override
    public IMatrix extractRow(int i) {
        IMatrix m = newInstance(1, getColsCount());

        for (int j = 0; j < getColsCount(); j++)
            m.set(0, j,  get(i, j));

        return m;
    }

    public IMatrix switchRows(int index1, int index2) {

        for (int i = 0; i < getColsCount(); i++) {
            double temp = get(index1, i);
            set(index1, i, get(index2, i));
            set(index2, i, temp);
        }

        return this;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        int n = getRowsCount();
        int m = getColsCount();

        for (int i = 0; i < n; i++) {
            // sb.append('[');
            for (int j = 0; j < m; j++) {
                sb.append(String.format("%6.2f ", get(i, j)));
            }
            sb.append("\n");
        }

        return sb.toString();
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) return false;
        if (this == obj) return true;
        if (!(obj instanceof IMatrix)) return false;

        IMatrix other = (IMatrix) obj;
        if (this.getRowsCount() != other.getRowsCount() ||
                this.getColsCount() != other.getColsCount())
            return false;

        for (int i = 0; i < getRowsCount(); i++)
            for (int j = 0; j < getColsCount(); j++) {
                double d1 = this.get(i, j);
                double d2 = other.get(i, j);
                if (Math.abs(d2 -d1) > EPSILON) return false;
            }


        return true;
    }

    @Override
    public void toFile(Path p) throws IOException {
        Files.writeString(p, toString());
    }

    public int[] initRowIndex() {
        int[] rowIndex = new int[getRowsCount()];
        for (int i = 0; i < getRowsCount(); i++)
            rowIndex[i] = i;

        return rowIndex;
    }

    private void checkDimensions(IMatrix other) {
        if (this.getColsCount() != other.getRowsCount())
            throw new IncompatableOperationException("These matrices cannot be multiplied.");
    }
}
