import numpy as np
from ga.solutions import DoubleArraySolution, BitArraySolution


def test_double_array_solution():
    lower = np.array([-5, -5, -5, 0, 0, 0])
    upper = np.array([5, 5, 5, 1, 1, 1])

    population = [DoubleArraySolution(6, lower, upper, True) for i in range(20)]

    print(type(population[0].arr[0]))

    for solution in population:
        assert all(lower <= solution.arr) and all(solution.arr <= upper), f'{solution} not in explicit constraint'


def test_bit_array_solution_decode():
    lower = np.array([0, -5])
    upper = np.array([1, 2])
    e = np.array([0.25, 1])

    solution = BitArraySolution(2, lower, upper, e, False)

    n = len(solution.arr)
    assert n == 6, f'Solution has {n} bits. Expected 6.'
    assert solution.number_of_bits[0] == 3
    assert solution.number_of_bits[1] == 3

    assert np.all(solution.decode() == np.array([0, -5]))

    solution.arr = np.array([1, 1, 1, 0, 1, 1], np.bool)
    assert np.all(solution.decode() == np.array([1, -2]))
