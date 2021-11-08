import math
import numpy as np

from ga.solutions import Solution

FORMAT = "[{:>6d}] best = {} fitness = {:10.6f} avg fitness = {:10.4f} population stdev = {:10.4f}"


class PeriodicPrinter:

    def __init__(self, n):
        self.n = n

    def __call__(self, ga, i, statistacs):
        if i % self.n != 0:
            return

        best = max(ga.population)
        print(FORMAT.format(i, best, best.fitness, statistacs['avg_fitness'], statistacs['population_std']))


class NewBestPrinter:

    def __init__(self):
        self.best = Solution()
        self.best.fitness = -math.inf

    def __call__(self, ga, i, statistacs):
        new_best = max(ga.population)
        if new_best > self.best:
            print(FORMAT.format(i, new_best, new_best.fitness, statistacs.get('avg_fitness', 0.0), statistacs.get('population_std', 0.0)))
            self.best = new_best


class ModifyMutationCallback:

    def __init__(self, population_std_threshold=1.0, p_solution_factor=1.0, p_variable_factor=1.0):
        self.population_std_threshold = population_std_threshold
        self.p_solution_factor = p_solution_factor
        self.p_variable_factor = p_variable_factor

    def __call__(self, ga, i, statistacs):
        if np.all(statistacs['population_std'] <= self.population_std_threshold):
            ga.mutation.p_solution *= self.p_solution_factor
            ga.mutation.p_variable *= self.p_variable_factor
