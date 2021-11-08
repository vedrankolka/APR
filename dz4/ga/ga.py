import numpy as np
from typing import List, Callable

from ga.functions import AbstractFunction
from ga.solutions import Solution
from ga.population.crossing import Crossing
from ga.population.mutation import Mutation
from ga.population.selection import Selection


class GeneticAlgorithm:
    f: AbstractFunction
    population: List[Solution]
    crossing: Crossing
    mutation: Mutation
    selection: Selection
    population_size: int
    max_evaluations: int
    max_iterations: int = 1000
    fitness_threshold: float = 1e-9
    callbacks: List[Callable] = []

    def __init__(self, f: AbstractFunction, population: List[Solution], crossing: Crossing,
                 mutation: Mutation, selection: Selection, population_size: int,
                 max_evaluations: int, max_iterations=1000, fitness_threshold=-1e-6, callbacks=[]):
        self.f = f
        self.population = population
        self.crossing = crossing
        self.mutation = mutation
        self.selection = selection
        self.population_size = population_size
        self.max_evaluations = max_evaluations
        self.max_iterations = max_iterations
        self.fitness_threshold = fitness_threshold
        self.callbacks = callbacks

    def solve(self, statistics=False, verbose=False):

        self.evaluate(self.population)
        statistacs = dict()

        for i in range(self.max_iterations):

            best = max(self.population)
            if best.fitness >= self.fitness_threshold:
                if verbose:
                    print('Finishing because fitness satisfies the threshold.')
                break

            self.selection.set_population(self.population)

            new_population = []
            # add children but leave room for the best from the previous population
            while len(new_population) < self.population_size - 1:
                momma, poppa = self.selection.select_parents()
                child = self.crossing.cross(momma, poppa)
                new_population.append(child)

            # new_population = list(new_population)
            # mutate all children with probability set in mutation object
            self.mutation.mutate_population(new_population)
            # ensure elitism
            new_population.append(max(self.population))
            self.population = new_population
            self.evaluate(self.population)

            if self.f.get_call_count() >= self.max_evaluations:
                if verbose:
                    print('Finishing because evaluation limit is reached.')
                break

            if statistics:
                statistacs['avg_fitness'] = np.mean([s.fitness for s in self.population])
                statistacs['population_std'] = np.std([s.decode() for s in self.population])

            if verbose:
                for callback in self.callbacks:
                    callback(self, i, statistacs)

        return max(self.population)

    def evaluate(self, population):
        for solution in population:
            solution.fitness = -self.f(solution.decode())
