import numpy as np
import math


class AbstractFunction:

    def __init__(self):
        self.call_count = 0

    def __call__(self, *args, **kwargs):
        self.call_count += 1
        return 0

    def get_call_count(self):
        return self.call_count

    def set_call_count(self, count):
        self.call_count = count

    def key(self, args):
        if isinstance(args[0], float):
            return args[0]
        else:
            return tuple(args[0])


class DerivableFunction(AbstractFunction):

    def __init__(self):
        super(DerivableFunction, self).__init__()
        self.gradient_call_count = 0
        self.hessian_call_count = 0

    def gradient(self, x) -> np.ndarray:
        self.gradient_call_count += 1

    def get_gradient_call_count(self):
        return self.gradient_call_count

    def hessian(self, x):
        self.hessian_call_count += 1

    def get_hessian_call_count(self):
        return self.hessian_call_count


class RosenbrocksBanana(DerivableFunction):
    """ Rosenbrocks "banana" function """

    def __call__(self, *args, **kwargs):
        super(RosenbrocksBanana, self).__call__()
        x1, x2 = self.key(args)
        return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2

    def key(self, args):
        return args[0][0], args[0][1]

    def gradient(self, x) -> np.ndarray:
        super(RosenbrocksBanana, self).gradient(x)
        # df/dx1 = 2 (-1 + x1 - 200 x1 x2 + 200 x1^3)
        df_dx1 = 2 * (-1 + x[0] - 200 * x[0] * x[1] + 200 * x[0] ** 3)
        # df/dx2 = 200 (x2 - x1^2)
        df_dx2 = 200 * (x[1] - x[0] ** 2)

        return np.array([df_dx1, df_dx2])

    def hessian(self, x):
        super(RosenbrocksBanana, self).hessian(x)
        dx1dx1 = 1200 * x[0] ** 2 - 400 * x[1] + 2
        dx1dx2 = -400 * x[0]
        dx2dx2 = 200

        return np.array([dx1dx1, dx1dx2, dx1dx2, dx2dx2]).reshape([2, 2])


class SimpleQuadraticFunction(DerivableFunction):
    """ A function in the form f(x1, x2) = a*(x1 - b)^2 + c*(x2 - d)^2 """

    def __init__(self, a, b, c, d):
        super(SimpleQuadraticFunction, self).__init__()
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.hesse = np.array([2 * a, 0, 0, 2 * c]).reshape([2, 2])

    def __call__(self, *args, **kwargs):
        super(SimpleQuadraticFunction, self).__call__()
        x1, x2 = self.key(args)
        return self.a * (x1 - self.b) ** 2 + self.c * (x2 - self.d) ** 2

    def key(self, args):
        return args[0][0], args[0][1]

    def gradient(self, x) -> np.ndarray:
        super(SimpleQuadraticFunction, self).gradient(x)
        df_dx1 = 2 * self.a * (x[0] - self.b)
        df_dx2 = 2 * self.c * (x[1] - self.d)
        return np.array([df_dx1, df_dx2])

    def hessian(self, x):
        super(SimpleQuadraticFunction, self).hessian(x)
        return self.hesse


F2 = lambda: SimpleQuadraticFunction(1, 4, 4, 2)
F3 = lambda: SimpleQuadraticFunction(1, 2, 1, -3)
F4 = lambda: SimpleQuadraticFunction(1, 3, 1, 0)


class Function2(DerivableFunction):

    def __init__(self):
        super(Function2, self).__init__()
        self.hesse = np.array([2, 0, 0, 8]).reshape([2, 2])

    def __call__(self, *args, **kwargs):
        super(Function2, self).__call__()
        x1, x2 = self.key(args)
        return (x1 - 4) ** 2 + 4 * (x2 - 2) ** 2

    def key(self, args):
        return args[0][0], args[0][1]

    def gradient(self, x) -> np.ndarray:
        super(Function2, self).gradient(x)
        # df/dx1 = 2 (x1 - 4)
        df_dx1 = 2 * (x[0] - 4)
        # df/dx2 = 8 * (x2 - 2)
        df_dx2 = 8 * (x[1] - 2)
        return np.array([df_dx1, df_dx2])


class Function3(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function3, self).__call__()
        x = x = np.array([args[0]]) if isinstance(args[0], float) else args[0]
        return sum([(x[i] - i) ** 2 for i in range(len(x))])


# samo za onaj jedan zadatak iz drugog labosa
class Function3Translated(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function3Translated, self).__call__()
        x = x = np.array([args[0]]) if isinstance(args[0], float) else args[0]
        return (x - 3) ** 2


class Function4(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function4, self).__call__()
        x1, x2 = self.key(args)
        return abs((x1 - x2) * (x1 + x2)) + np.sqrt(x1 ** 2 + x2 ** 2)

    def key(self, args):
        return args[0][0], args[0][1]


class Function6(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function6, self).__call__()
        x = np.array([args[0]]) if isinstance(args[0], float) else args[0]
        sum_squared = sum([xi * xi for xi in x])
        return 0.5 + (math.sin(math.sqrt(sum_squared)) ** 2 - 0.5) \
               / (1 + 0.001 * sum_squared) ** 2


class CacheFunctionProxy(AbstractFunction):

    def __init__(self, f):
        super(CacheFunctionProxy, self).__init__()
        self.f = f
        self.cache = dict()

    def __call__(self, *args, **kwargs):
        key = self.f.key(args)
        value = self.cache.get(key)

        if value is None:
            value = self.f(*args, **kwargs)
            self.cache[key] = value

        return value

    def get_call_count(self):
        return self.f.get_call_count()

    def set_call_count(self, count):
        self.f.set_call_count(count)


class TransformedFunction(AbstractFunction):

    def __init__(self, f: AbstractFunction, inequality_constraints, equality_constraints):
        super(TransformedFunction, self).__init__()
        self.t = 1.0
        self.inequality_constraints = inequality_constraints
        self.equality_constraints = equality_constraints
        self.f = f

    def __call__(self, *args, **kwargs):
        punishment = 0.0
        for ic in self.inequality_constraints:
            value = ic(args[0])
            if value <= 0:
                punishment += 1e12
            else:
                punishment -= 1 / self.t * np.log(value)

        for ec in self.equality_constraints:
            try:
                greska_na_kva = (ec(args[0])**2)
                value = greska_na_kva * self.t
                punishment += self.t * (ec(args[0])**2)
            except Exception:
                print(greska_na_kva)
                print(value)
                print(punishment)

        return self.f(*args, **kwargs) + punishment


class ExplicitContraint:

    def __init__(self, xmin, xmax):
        self.xmin = xmin
        self.xmax = xmax

    def __call__(self, x):
        x = np.array(x)
        return all(self.xmin <= x) and all(x <= self.xmax)


class LinearConstraint:

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def __call__(self, x):
        return self.a * x[0] + self.b * x[1] + self.c


# za 3. i 4. zadatak
g1 = LinearConstraint(-1, 1, 0)
g2 = LinearConstraint(-1, 0, 2)
# za 5. zadatak
g3 = LinearConstraint(-1, -1, 3)
g4 = LinearConstraint(1.5, -1, 3)
h1 = LinearConstraint(0, 1, -1)
