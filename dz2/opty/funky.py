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


class Function1(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function1, self).__call__()
        x1, x2 = self.key(args)
        return 100 * (x2 - x1**2)**2 + (1 - x1)**2

    def key(self, args):
        return args[0][0], args[0][1]


class Function2(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function2, self).__call__()
        x1, x2 = self.key(args)
        return (x1 - 4)**2 + 4*(x2 - 2)**2

    def key(self, args):
        return args[0][0], args[0][1]


class Function3(AbstractFunction):
    
    def __call__(self, *args, **kwargs):
        super(Function3, self).__call__()
        x = x = np.array([args[0]]) if isinstance(args[0], float) else args[0]
        return sum([(x[i]-i)**2 for i in range(len(x))])

#    def key(self, args):
#        return tuple(args[0])


class Function3Translated(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function3Translated, self).__call__()
        x = x = np.array([args[0]]) if isinstance(args[0], float) else args[0]
        return (x-3)**2

 #   def key(self, args):
 #       return tuple(args[0])

class Function4(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function4, self).__call__()
        x1, x2 = self.key(args)
        return abs((x1-x2)*(x1+x2)) + np.sqrt(x1**2+x2**2)

    def key(self, args):
        return args[0][0], args[0][1]


class Function6(AbstractFunction):

    def __call__(self, *args, **kwargs):
        super(Function6, self).__call__()
        x = np.array([args[0]]) if isinstance(args[0], float) else args[0]
        sum_squared = sum([xi*xi for xi in x])
        return 0.5 + (math.sin(math.sqrt(sum_squared))**2-0.5)\
               / (1 + 0.001 * sum_squared)**2

 #   def key(self, args):
 #       return tuple(args[0])


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
