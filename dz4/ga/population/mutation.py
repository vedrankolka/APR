import numpy as np

from ga.solutions import BitArraySolution, DoubleArraySolution, Solution


class Mutation:

    def __init__(self, p_solution):
        self.p_solution = p_solution

    def mutate_population(self, solutions):
        for solution in solutions:
            if np.random.random(1) < self.p_solution:
                self.mutate_solution(solution)

    def mutate_solution(self, solution: Solution):
        pass


class OneBitMutation(Mutation):

    def __init__(self, p_solution, p_bit):
        super(OneBitMutation, self).__init__(p_solution)
        self.p_bit = p_bit

    def mutate_solution(self, solution: BitArraySolution):
        p = np.random.uniform(0, 1, len(solution.arr))
        solution.arr[p < self.p_bit] = np.logical_not(solution.arr[p < self.p_bit])

        return solution


class DoubleGaussMutation(Mutation):

    def __init__(self, p_solution, p_variable, sigma):
        super(DoubleGaussMutation, self).__init__(p_solution)
        self.p_variable = p_variable
        self.sigma = sigma

    def mutate_solution(self, solution:DoubleArraySolution):
        to_mutate = np.random.uniform(0, 1, len(solution.arr)) < self.p_variable
        solution.arr[to_mutate] = np.random.normal(solution.arr[to_mutate], self.sigma, len(solution.arr[to_mutate]))
        return solution.set_arr(solution.arr)
