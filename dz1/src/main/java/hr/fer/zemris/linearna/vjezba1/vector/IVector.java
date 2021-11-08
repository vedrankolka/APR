package hr.fer.zemris.linearna.vjezba1.vector;

import hr.fer.zemris.linearna.vjezba1.matrix.IMatrix;

public interface IVector {

    double get(int i);
    IVector set(int i, double d);
    int getDimension();
    IVector copy();
    IVector copyPart(int i);
    IVector newInstance(int i);
    IVector add(IVector v);
    IVector nAdd(IVector v);
    IVector sub(IVector v);
    IVector nSub(IVector v);
    IVector scalarMultiply(double d);
    IVector nScalarMultiply(double d);
    double norm();
    IVector normalize();
    IVector nNormalize();
    double cosine(IVector v);
    double scalarProduct(IVector v);
    IVector nVectorProduct(IVector v);
    IVector nFromHomogeneus();
    IMatrix toRowMatrix(boolean b);
    IMatrix toColumnMatrix(boolean b);
    double[] toArray();

}
