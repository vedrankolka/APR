package hr.fer.zemris.linearna.vjezba1.vector;

import hr.fer.zemris.linearna.vjezba1.IncompatableOperationException;

import java.util.Arrays;

public class Vector extends AbstractVector {

    private double[] elements;
    private int dimension;
    private boolean readOnly;

    public Vector(double ...elements) {
        this(false, false, elements);
    }

    public Vector(boolean readOnly, boolean takeElements, double ...elements) {

        if (takeElements)
            this.elements = elements;
        else
            this.elements = Arrays.copyOf(elements, elements.length);

        this.readOnly = readOnly;
        this.dimension = elements.length;
    }

    @Override
    public double get(int i) {
        return elements[i];
    }

    @Override
    public IVector set(int i, double d) {
        checkReadOnly();
        elements[i] = d;
        return this;
    }

    @Override
    public int getDimension() {
        return dimension;
    }

    @Override
    public IVector copy() {
        return new Vector(elements);
    }

    @Override
    public IVector copyPart(int i) {
        // TODO
        throw new IncompatableOperationException("Not implemented yet.");
    }

    @Override
    public IVector newInstance(int i) {
        return new Vector(false, true, new double[i]);
    }

    public static IVector parseSimple(String s) {
        String[] parts = s.trim().split("\\s+");
        double[] elements = new double[parts.length];

        for (int i = 0; i < elements.length; i++) elements[i] = Double.parseDouble(parts[i]);

        return new Vector(false, true, elements);
    }

    private void checkReadOnly() {
        if (readOnly)
            throw new IncompatableOperationException("This vector is read-only.");
    }

}
