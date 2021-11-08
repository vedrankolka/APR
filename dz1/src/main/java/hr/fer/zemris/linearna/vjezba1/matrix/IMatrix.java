package hr.fer.zemris.linearna.vjezba1.matrix;

import hr.fer.zemris.linearna.vjezba1.vector.IVector;

import java.io.IOException;
import java.nio.file.Path;

public interface IMatrix {

    int getRowsCount();
    int getColsCount();
    double get(int i, int j);
    IMatrix set(int i, int j, double d);
    IMatrix copy();
    IMatrix newInstance(int i, int j);
    IMatrix nTranspose(boolean b);
    IMatrix add(IMatrix m);
    IMatrix nAdd(IMatrix m);
    IMatrix sub(IMatrix m);
    IMatrix nSub(IMatrix m);
    IMatrix nMultiply(IMatrix m);
    double determinant();
    IMatrix subMatrix(int i, int j, boolean b);
    IMatrix nInvert();
    double[][] toArray();
    IVector toVector(boolean b);
    IMatrix extractRow(int i);
    IMatrix switchRows(int[] index);
    void toFile(Path path) throws IOException;

}
