package hr.fer.zemris.linearna.vjezba1;

public class IncompatableOperationException extends RuntimeException {

    public IncompatableOperationException(String message) {
        super(message);
    }

    public IncompatableOperationException() {
    }

    public IncompatableOperationException(String s, Throwable throwable) {
        super(s, throwable);
    }

    public IncompatableOperationException(Throwable throwable) {
        super(throwable);
    }

}
