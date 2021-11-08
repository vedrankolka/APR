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

    def __call__(self, x):
        super(RosenbrocksBanana, self).__call__()
        x1, x2 = x[0], x[1]
        return 100 * (x2 - x1 ** 2) ** 2 + (1 - x1) ** 2

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


class Function3(AbstractFunction):

    def __call__(self, x):
        super(Function3, self).__call__()
        x = np.array(x)
        return sum([(x[i] - (i+1)) ** 2 for i in range(len(x))])


class SchaffersFunction(AbstractFunction):

    def __call__(self, x):
        super(SchaffersFunction, self).__call__()
        x = np.array(x)
        sum_squared = sum(x * x)
        return 0.5 + (math.sin(math.sqrt(sum_squared)) ** 2 - 0.5) \
               / (1 + 0.001 * sum_squared) ** 2


class AlmostSchaffers(AbstractFunction):

    def __call__(self, x):
        super(AlmostSchaffers, self).__call__()
        x = np.array(x)
        ss = sum(x * x)
        return ss**0.25 * (1 + math.sin(50 * ss**0.1)**2)


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
