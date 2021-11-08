package hr.fer.zemris.linearna.vjezba1.vector;

import hr.fer.zemris.linearna.vjezba1.matrix.IMatrix;
import hr.fer.zemris.linearna.vjezba1.IncompatableOperationException;

public abstract class AbstractVector implements IVector {

    public AbstractVector() {
    }

    public IVector add(IVector other) {
        checkDimensions(other);

        for (int i = this.getDimension() - 1; i >= 0; i--)
            this.set(i, this.get(i) + other.get(i));

        return this;
    }

    public IVector nAdd(IVector v) {
        return copy().add(v);
    }

    public IVector sub(IVector other) {
        checkDimensions(other);

        for (int i = this.getDimension() - 1; i >= 0; i--)
            this.set(i, this.get(i) - other.get(i));

        return this;
    }

    public IVector nSub(IVector v) {
        return copy().sub(v);
    }

    public IVector scalarMultiply(double d) {
        for (int i = this.getDimension() - 1; i >= 0; i--)
            this.set(i, this.get(i) * d);

        return this;
    }

    public IVector nScalarMultiply(double d) {
        return copy().scalarMultiply(d);
    }

    public double norm() {
        int n = getDimension();
        double sum = 0.0;
        for (int i = 0; i < n; i++) {
            double value = get(i);
            sum += value * value;
        }

        return Math.sqrt(sum);
    }

    public IVector normalize() {
        double norm = norm();
        for (int i = this.getDimension() - 1; i >= 0; i--) {
            set(i, get(i) / norm);
        }

        return this;
    }

    public IVector nNormalize() {
        return copy().normalize();
    }

    public double cosine(IVector v) {
        return scalarProduct(v) / this.norm() / v.norm();
    }

    public double scalarProduct(IVector v) {
        double sum = 0.0;
        for (int i = this.getDimension() - 1; i >= 0; i--) {
            sum += this.get(i) * v.get(i);
        }

        return sum;
    }

    public IVector nVectorProduct(IVector v) {
        if (this.getDimension() != 3 || v.getDimension() != 3)
            throw new IncompatableOperationException("Vector product is defined only for 3D vectors.");

        double x1 = this.get(0);
        double y1 = this.get(1);
        double z1 = this.get(2);
        double x2 = v.get(0);
        double y2 = v.get(1);
        double z2 = v.get(2);

        double x = y1 * z2 - z1 * y2;
        double y = z1 * x2 - x1 * z2;
        double z = x1 * y2 - y1 * x2;

        return newInstance(3).set(0, x).set(1, y).set(2, z);
    }

    public IVector nFromHomogeneus() {
        IVector v = newInstance(getDimension() - 1);
        double h = get(getDimension() - 1);
        for (int i = 0; i < getDimension() - 1; i++)
            v.set(i, get(i) / h);

        return v;
    }

    // TODO
    public IMatrix toRowMatrix(boolean b) {
        return null;
    }

    // TODO
    public IMatrix toColumnMatrix(boolean b) {
        return null;
    }

    public double[] toArray() {
        double[] values = new double[getDimension()];

        for (int i = 0; i < values.length; i++)
            values[i] = get(i);

        return values;
    }

    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();

        sb.append('[');
        for (int i = 0; i < getDimension(); i++)
            sb.append(String.format("%6.2f ", get(i)));
        sb.append(']');

        return sb.toString();
    }

    private void checkDimensions(IVector other) {
        if(this.getDimension()!=other.getDimension())
            throw new IncompatableOperationException();
    }
}
