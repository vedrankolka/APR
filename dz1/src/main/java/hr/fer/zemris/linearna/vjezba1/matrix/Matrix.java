package hr.fer.zemris.linearna.vjezba1.matrix;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

public class Matrix extends AbstractMatrix {

    protected double[][] elements;
    protected int rows;
    protected int cols;

    public Matrix(int rows, int cols) {
        this(rows, cols, new double[rows][cols], true);
    }

    public Matrix(int rows, int cols, double[][] elements, boolean live) {
        this.rows = rows;
        this.cols = cols;
        if (live) {
            this.elements = elements;
        } else {
            this.elements = new double[rows][cols];
            for (int i = 0; i < rows; i++)
                for (int j = 0; j < cols; j++)
                    this.elements[i][j] = elements[i][j];
        }
    }

    @Override
    public int getRowsCount() {
        return rows;
    }

    @Override
    public int getColsCount() {
        return cols;
    }

    @Override
    public double get(int i, int j) {
        return elements[i][j];
    }

    @Override
    public IMatrix set(int i, int j, double d) {
        if (Math.abs(d) < EPSILON) d = 0;
        elements[i][j] = d;
        return this;
    }

    @Override
    public IMatrix copy() {
        return new Matrix(rows, cols, elements, false);
    }

    @Override
    public IMatrix newInstance(int i, int j) {
        return new Matrix(i, j);
    }

    public static IMatrix parseSimple(String s) {
        String[] stringRows = s.trim().split("\\|");
        return parseRows(stringRows);
    }

    public static IMatrix fromFile(Path path) throws IOException {
        String[] stringRows = Files.readString(path).split("\n");
        return parseRows(stringRows);
    }

    public static IMatrix parseRows(String[] stringRows) {
        double[][] elements = null;
        int n = stringRows.length;
        int m = 0;
        for (int i = 0; i < n; i++) {
            String[] columns = stringRows[i].trim().split("\\s+");
            if (i == 0) {
                m = columns.length;
                elements = new double[n][m];
            }
            for (int j = 0; j < m; j++) {
                elements[i][j] = Double.parseDouble(columns[j]);
            }
        }

        if (m == n) return new SquareMatrix(n, elements, true);
        else return new Matrix(n, m, elements, true);
    }

    /**
     * The method returns a matrix of one column, with <code>n</code> rows.
     * All elements are 0, except for element in row <code>i</code> which is 1.
     * @param n - number of rows
     * @param i - index of non zero element
     * @return nx1 matrix where all elements are 0 except the i-th element which is 1
     */
    public static IMatrix e(int n, int i) {
        double[][] data = new double[n][1];

        for (int j = 0; j < n; j++)
            data[j][0] = j == i ? 1 : 0;

        return new Matrix(n, 1, data, true);
    }
}
