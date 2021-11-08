import numpy as np

from ga.solutions import DoubleArraySolution, BitArraySolution, Solution


class Crossing:

    def cross(self, momma: Solution, poppa: Solution):
        pass


class GaussCrossing(Crossing):

    def cross(self, momma: DoubleArraySolution, poppa: DoubleArraySolution):
        minimum = np.minimum(momma.arr, poppa.arr)
        maximum = np.maximum(momma.arr, poppa.arr)
        deltas = maximum - minimum
        arr = np.random.normal(minimum + deltas / 2, deltas / 2, len(momma.arr))

        return momma.new_like_me().set_arr(arr)


class BLXalphaCrossing(Crossing):

    def __init__(self, alpha):
        self.alpha = alpha

    def cross(self, momma: DoubleArraySolution, poppa: DoubleArraySolution):
        alphas = self.alpha * np.ones(len(momma.arr))
        arr = []
        for i in range(len(momma.arr)):
            arr.append(blxAlpha(momma.arr[i], poppa.arr[i], alphas[i]))

        return momma.new_like_me().set_arr(arr)


class UniformCrossing(Crossing):

    def cross(self, momma: BitArraySolution, poppa: BitArraySolution):
        r = np.random.choice([True, False], len(momma.arr))
        a = momma.arr
        b = poppa.arr
        # C = A*B + R*(A xor B)
        arr = np.logical_or(np.logical_and(a, b), np.logical_and(r, np.logical_xor(a, b)))
        return momma.new_like_me().set_arr(arr)


class OnePointCrossing(Crossing):

    def cross(self, momma: BitArraySolution, poppa: BitArraySolution):
        point = np.random.choice(list(range(1, len(momma.arr))))
        arr = []
        for i in range(point):
            arr.append(momma.arr[i])
        for i in range(point, len(momma.arr)):
            arr.append(poppa.arr[i])

        return momma.new_like_me().set_arr(np.array(arr))


def blxAlpha(a, b, alpha):
    minimum = min(a, b)
    maximum = max(a, b)
    delta = alpha * (maximum - minimum)

    return minimum - delta + np.random.uniform(0.0, 1.0, 1) * (maximum + 2 * delta - minimum)
