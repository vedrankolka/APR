import numpy as np


class Selection:

    def select_parents(self):
        pass

    def set_population(self, population):
        pass

    def update(self, population):
        pass


class RouletteWheelSelection(Selection):

    def __init__(self, n, minimum_effective_fitnes=0.0):
        self.minimum_effective_fitness = minimum_effective_fitnes
        self.population = np.zeros(n)
        self.effective_fitnesses = np.zeros(n)
        self.probabilities = np.zeros(n)

    def select_parents(self):
        index_of_momma = RouletteWheelSelection.choose(self.probabilities, 1)
        momma_probability = self.probabilities[index_of_momma]
        if not isinstance(momma_probability, float):
            print('wtf')
        self.probabilities[index_of_momma] = 0.0
        scale = 1 - momma_probability
        index_of_poppa = RouletteWheelSelection.choose(self.probabilities, scale)

        self.probabilities[index_of_momma] = momma_probability

        return self.population[index_of_momma], self.population[index_of_poppa]

    def set_population(self, population):
        self.population = population
        self.update(population)

    def update(self, old_population):
        fitness_sum = 0.0
        f_worst = min(old_population).fitness - self.minimum_effective_fitness

        for i in range(len(old_population)):
            self.effective_fitnesses[i] = old_population[i].fitness - f_worst
            fitness_sum += self.effective_fitnesses[i]

        self.probabilities = self.effective_fitnesses / fitness_sum

        if not isinstance(self.probabilities[0], float):
            print('jebo me pas')

    @staticmethod
    def choose(probabilities, scale):
        acc = 0.0
        try:
            p = np.random.uniform(0, scale, 1)
        except ValueError:
            print(scale)
            print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')

        for i in range(len(probabilities)):
            acc += probabilities[i]
            if p <= acc:
                return i

        raise RuntimeError('No one was chosen!\nprobabilities:', probabilities, '\nscale', scale)
