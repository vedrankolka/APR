import numpy as np

from functools import total_ordering


@total_ordering
class Solution:
    fitness: float

    def __init__(self):
        self.fitness = None

    def __lt__(self, other):
        return self.fitness < other.fitness


class DoubleArraySolution(Solution):

    def __init__(self, n=1, lower=0.0, upper=1.0, random=False, arr=None):
        super(DoubleArraySolution, self).__init__()
        if arr is None:
            self.lower = lower * np.ones(n, np.float64)
            self.upper = upper * np.ones(n, np.float64)
            if random is False:
                self.arr = self.lower * 1.0
            else:
                self.arr = self.randomize(n)
        else:
            n = len(arr)
            self.lower = lower * np.ones(n, np.float64)
            self.upper = upper * np.ones(n, np.float64)
            self.arr = arr

    def new_like_me(self):
        return DoubleArraySolution(len(self.arr), self.lower, self.upper)

    def copy(self):
        return DoubleArraySolution(lower=self.lower, upper=self.upper, arr=self.arr[:])

    def randomize(self, n):
        return self.lower + np.random.uniform(0.0, 1.0, n) * (self.upper - self.lower)

    def decode(self):
        return self.arr

    def __repr__(self):
        return '[' + ', '.join('{:>10.6f}'.format(x) for x in self.arr) + ']'

    def set_arr(self, arr):
        for i in range(len(arr)):
            self.arr[i] = min(max(self.lower[i], arr[i]), self.upper[i])

        return self


def randomize(n):
    return np.random.choice([True, False], n)


class BitArraySolution(Solution):

    def __init__(self, n_variables=1, lower=0.0, upper=1.0, e=1e-6, random=False, arr=None, number_of_bits=None):
        """

        :param n_variables: number of variables
        :param lower: lower boundry for each variable
        :param upper: upper boundry for each variable
        :param e: wanted precision
        :param random: boolean to indicate if the created solution should be randomized
        :param arr: array of values to use as own
        """
        super(BitArraySolution, self).__init__()
        self.lower = np.ones(n_variables) * lower
        self.upper = np.ones(n_variables) * upper
        # a little hack, maybe fix this
        if number_of_bits is not None:
            self.number_of_bits = number_of_bits
        else:
            number_of_bits = np.ceil(np.log2((self.upper - self.lower) / e) + 0.001)
            self.number_of_bits = np.array(number_of_bits, np.int)

        n = int(sum(number_of_bits))
        if arr is None:
            if random is False:
                self.arr = np.zeros(n, np.bool)
            else:
                self.arr = randomize(n)
        else:
            self.arr = arr

    def new_like_me(self):
        return BitArraySolution(len(self.number_of_bits), self.lower, self.upper, number_of_bits=self.number_of_bits)

    def copy(self):
        return BitArraySolution(len(self.number_of_bits), self.lower, self.upper, arr=self.arr[:],
                                number_of_bits=self.number_of_bits)

    def decode(self):
        nbd = []
        i = 0
        for j in self.number_of_bits:
            nbd.append(nbc_decode(self.arr[i:(i + j)]))
            i += j

        nbd = np.array(nbd)
        nbd = self.lower + (self.upper - self.lower) * nbd / (2 ** self.number_of_bits - 1)
        return nbd

    def __repr__(self):
        return '[' + ', '.join('{:>10.6f}'.format(x) for x in self.decode()) + ']'

    def set_arr(self, arr):
        self.arr[:] = arr
        return self


def nbc_decode(array):
    a = 0
    n = len(array) - 1
    for i, bit in enumerate(array):
        a += bit * 2 ** (n - i)
    return a
