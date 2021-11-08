import numpy as np


class Integrator:

    def __init__(self, A, B=0, step=0.01, r=lambda t: 1):
        self.A = A
        self.B = B
        self.step = step
        self.r = r

    def integrate(self, x0, start, end, callbacks=[], v=100):
        xs = [x0]
        ts = [start]
        x = x0
        t = start + self.step
        i = 0
        while t <= end:
            x = self.next(x, t)
            xs.append(x)
            ts.append(t)
            t += self.step
            if v is not None and i % v == 0:
                for callback in callbacks:
                    callback(x)
            i += 1

        return np.array(xs), np.array(ts)

    def next(self, x, t):
        pass


class ImplicitIntegrator(Integrator):

    def next_implicit(self, x, t, x_next_predicted):
        pass


class EulerIntegrator(Integrator):

    def next(self, x, t):
        delta_x = (self.A @ x + self.B * self.r(t)) * self.step
        return x + delta_x


class ReversedEulerIntegrator(ImplicitIntegrator):

    def __init__(self, A, B=0, step=0.01, r=lambda t: 1):
        super(ReversedEulerIntegrator, self).__init__(A, B, step, r)
        n = A.shape[0]
        I = np.identity(n)
        P = np.linalg.inv((I - step * A))
        self.P = P
        self.Q = P @ (step * B)

    def next(self, x, t):
        return self.P @ x + self.Q * self.r(t + self.step)

    def next_implicit(self, x, t, x_next_predicted):
        delta_x = self.step * (self.A @ x_next_predicted + self.B * self.r(t + self.step))
        return x + delta_x


class TrapezeIntegrator(ImplicitIntegrator):

    def __init__(self, A, B=0, step=0.01, r=lambda t: 1):
        super(TrapezeIntegrator, self).__init__(A, B, step, r)
        n = A.shape[0]
        I = np.identity(n)
        P = np.linalg.inv(I - A * step/2)
        self.R = P @ (I + A * step/2)
        self.S = P @ (step/2 * B)

    def next(self, x, t):
        return self.R @ x + self.S * (self.r(t) + self.r(t + self.step))

    def next_implicit(self, x, t, x_next_predicted):
        delta_x = self.step/2 * (self.A @ x + self.B * self.r(t) + self.A @ x_next_predicted + self.B * self.r(t + self.step))
        return x + delta_x


class RungeKutta4Real(Integrator):

    def __init__(self, A, B=0, step=0.01, r=lambda t: 1):
        super(RungeKutta4Real, self).__init__(A, B, step, r)

    def __f(self, x, t):
        return self.A @ x + self.B * self.r(t)

    def next(self, x, t):
        T = self.step
        m1 = self.__f(x, t)
        m2 = self.__f(x + T/2 * m1, t + T/2)
        m3 = self.__f(x + T/2 * m2, t + T/2)
        m4 = self.__f(x + T*m3, t + T)

        return x + T/6 * (m1 + 2*m2 + 2*m3 + m4)


class PECEIntegrator(Integrator):

    def __init__(self, predictor: Integrator, corrector: ImplicitIntegrator, s: int):
        self.predictor = predictor
        self.corrector = corrector
        self.s = s
        self.step = predictor.step

    def next(self, x, t):
        x_next = self.predictor.next(x, t)
        for i in range(self.s):
            x_next = self.corrector.next_implicit(x, t, x_next)

        return x_next
