import numpy as np
import sys
import shutil
import pandas
import matplotlib.pyplot as plt

from configparser import ConfigParser

from ga.callbacks import PeriodicPrinter, ModifyMutationCallback, NewBestPrinter
from ga.functions import RosenbrocksBanana, CacheFunctionProxy, SchaffersFunction, AlmostSchaffers
from ga.ga import GeneticAlgorithm
from ga.population.selection import RouletteWheelSelection
from ga.solutions import DoubleArraySolution, BitArraySolution
from ga.population.crossing import GaussCrossing, BLXalphaCrossing, UniformCrossing, OnePointCrossing
from ga.population.mutation import OneBitMutation, DoubleGaussMutation

# read hyperparameters
from ga.functions import Function3

params = ConfigParser()
params.read(sys.argv[1])

interactive_mode = '-i' in sys.argv
verbose = '-v' in sys.argv
statistics = '-s' in sys.argv

p_solution = params['M'].getfloat('p_solution')
p_variable = params['M'].getfloat('p_variable')
sigma = params['M'].getfloat('sigma')

population_size = params['P'].getint('population_size')
epsilon = params['P'].getfloat('epsilon')

alpha = params['C'].getfloat('alpha')

minimum_efective_fitness = params['S'].getfloat('minimum_effective_fitness')

max_evaluations = params['GA'].getint('max_evaluations')
max_iterations = params['GA'].getint('max_iterations')
fitness_threshold = params['GA'].getfloat('fitness_threshold')

# =================== ZAD 1 =====================
lower = params['ZAD1'].getfloat('lower')
upper = params['ZAD1'].getfloat('upper')

selection = RouletteWheelSelection(population_size, minimum_efective_fitness)
double_crossing = GaussCrossing()
double_mutation = DoubleGaussMutation(p_solution, p_variable, sigma)
bit_crossing = OnePointCrossing()
bit_mutation = OneBitMutation(p_solution, p_variable)


def solve_function_double(f, population):
    callbacks = [NewBestPrinter()]
    ga = GeneticAlgorithm(f, population, double_crossing, double_mutation, selection, population_size,
                          max_evaluations, max_iterations, fitness_threshold, callbacks)

    best_solution = ga.solve(statistics=statistics, verbose=verbose)
    print(best_solution, f(best_solution.decode()))
    return best_solution


def solve_function_bit(f, population):
    callbacks = [NewBestPrinter()]
    ga = GeneticAlgorithm(f, population, bit_crossing, bit_mutation, selection, population_size,
                          max_evaluations, max_iterations, fitness_threshold, callbacks)

    best_solution = ga.solve(statistics=statistics, verbose=verbose)
    print(best_solution, f(best_solution.decode()))
    return best_solution


print('============================ ZAD1 ==========================')

print('Rosenbrocks banana function')
print('Double array')
double_population = [DoubleArraySolution(2, lower, upper, True) for i in range(population_size)]
solve_function_double(RosenbrocksBanana(), double_population)

print('Bit vector')
bit_population = [BitArraySolution(2, lower, upper, epsilon, True) for i in range(population_size)]
solve_function_bit(RosenbrocksBanana(), bit_population)

print('Second function')
print('Double array')
double_population = [DoubleArraySolution(5, lower, upper, True) for i in range(population_size)]
solve_function_double(Function3(), double_population)

print('Bit vector')
bit_population = [BitArraySolution(5, lower, upper, epsilon, True) for i in range(population_size)]
solve_function_bit(Function3(), bit_population)

print('Schaffers function')
print('Double array')
double_population = [DoubleArraySolution(2, lower, upper, True) for i in range(population_size)]
solve_function_double(SchaffersFunction(), double_population)

print('Bit vector')
bit_population = [BitArraySolution(2, lower, upper, epsilon, True) for i in range(population_size)]
solve_function_bit(SchaffersFunction(), bit_population)

print('Almost Schaffers function')
print('Double array')
double_population = [DoubleArraySolution(2, lower, upper, True) for i in range(population_size)]
solve_function_double(AlmostSchaffers(), double_population)

print('Bit vector')
bit_population = [BitArraySolution(2, lower, upper, epsilon, True) for i in range(population_size)]
solve_function_bit(AlmostSchaffers(), bit_population)

print('============================ ZAD2 ==========================')

dimensions = [1, 3, 6, 10]
# dimensions = []

for d in dimensions:
    print('\ndimension =', d, '\n')
    double_population = [DoubleArraySolution(d, lower, upper, True) for i in range(population_size)]
    solve_function_double(SchaffersFunction(), double_population)

    double_population = [DoubleArraySolution(d, lower, upper, True) for i in range(population_size)]
    solve_function_double(AlmostSchaffers(), double_population)

print('============================ ZAD3 ==========================')

bf_3_double_schaffers = []
bf_3_bit_schaffers = []
bf_6_double_schaffers = []
bf_6_bit_schaffers = []

bf_3_double_almost_schaffers = []
bf_3_bit_almost_schaffers = []
bf_6_double_almost_schaffers = []
bf_6_bit_almost_schaffers = []

max_evaluations = 1e5
epsilon = 1e-4

lower = -25
upper = 25

for i in range(10):
    double_population = [DoubleArraySolution(3, lower, upper, True) for i in range(population_size)]
    bf_3_double_schaffers.append(solve_function_double(CacheFunctionProxy(SchaffersFunction()), double_population).fitness)

    double_population = [DoubleArraySolution(3, lower, upper, True) for i in range(population_size)]
    bf_3_double_almost_schaffers.append(solve_function_double(CacheFunctionProxy(AlmostSchaffers()), double_population).fitness)

    double_population = [DoubleArraySolution(6, lower, upper, True) for i in range(population_size)]
    bf_6_double_schaffers.append(solve_function_double(CacheFunctionProxy(SchaffersFunction()), double_population).fitness)

    double_population = [DoubleArraySolution(6, lower, upper, True) for i in range(population_size)]
    bf_6_double_almost_schaffers.append(solve_function_double(CacheFunctionProxy(AlmostSchaffers()), double_population).fitness)

    bit_population = [BitArraySolution(3, lower, upper, epsilon, True) for i in range(population_size)]
    bf_3_bit_schaffers.append(solve_function_bit(CacheFunctionProxy(SchaffersFunction()), bit_population).fitness)

    bit_population = [BitArraySolution(3, lower, upper, epsilon, True) for i in range(population_size)]
    bf_3_bit_almost_schaffers.append(solve_function_bit(CacheFunctionProxy(AlmostSchaffers()), bit_population).fitness)

    bit_population = [BitArraySolution(6, lower, upper, epsilon, True) for i in range(population_size)]
    bf_6_bit_schaffers.append(solve_function_bit(CacheFunctionProxy(SchaffersFunction()), bit_population).fitness)

    bit_population = [BitArraySolution(6, lower, upper, epsilon, True) for i in range(population_size)]
    bf_6_bit_almost_schaffers.append(solve_function_bit(CacheFunctionProxy(AlmostSchaffers()), bit_population).fitness)


# np.save('zad3_data2/3_variables_bitvector_schaffers.npy', np.array(bf_3_bit_schaffers))
# np.save('zad3_data2/6_variables_bitvector_schaffers.npy', np.array(bf_6_bit_schaffers))
# np.save('zad3_data2/3_variables_doubles_schaffers.npy', np.array(bf_3_double_schaffers))
# np.save('zad3_data2/6_variables_doubles_schaffers.npy', np.array(bf_6_double_schaffers))
# np.save('zad3_data2/3_variables_bitvector_almost_schaffers.npy', np.array(bf_3_bit_almost_schaffers))
# np.save('zad3_data2/6_variables_bitvector_almost_schaffers.npy', np.array(bf_6_bit_almost_schaffers))
# np.save('zad3_data2/3_variables_doubles_almost_schaffers.npy', np.array(bf_3_double_almost_schaffers))
# np.save('zad3_data2/6_variables_doubles_almost_schaffers.npy', np.array(bf_6_double_almost_schaffers))

population_sizes = [30, 50, 100, 200]
mutation_probabilities = [0.1, 0.3, 0.6, 0.9]

population_sizes_best_fitnesses = [[], [], [], []]

for i in range(0): # len(population_sizes)

    for j in range(10):
        double_population = [DoubleArraySolution(2, lower, upper, True) for k in range(population_sizes[i])]
        selection = RouletteWheelSelection(population_sizes[i], minimum_efective_fitness)
        mutation = DoubleGaussMutation(mutation_probabilities[0], p_variable, sigma)
        best = solve_function_double(SchaffersFunction(), double_population)
        population_sizes_best_fitnesses[i].append(best.fitness)

medians = [np.median(bf) for bf in population_sizes_best_fitnesses]
data = np.array(population_sizes_best_fitnesses).reshape(4, 10)
np.save('zad4_po_populacijama.npy', data)

data = np.transpose(data)
df = pandas.DataFrame(data, columns=[population_sizes])
df.boxplot()
plt.savefig('population_sizes_boxplot.jpg')

best_size_index = 0
for i in range(1, 4):
    if medians[i] > medians[best_size_index]:
        best_size_index = i

best_population_size = population_sizes[best_size_index]
print('best population size is', best_population_size)

mutation_probabilities_best_fitnesses = [[], [], [], []]

for i in range(len(mutation_probabilities)):

    for j in range(10):
        double_population = [DoubleArraySolution(2, lower, upper, True) for k in range(best_population_size)]
        selection = RouletteWheelSelection(best_population_size, minimum_efective_fitness)
        mutation = DoubleGaussMutation(mutation_probabilities[i], p_variable, sigma)
        best = solve_function_double(SchaffersFunction(), double_population)
        mutation_probabilities_best_fitnesses[i].append(best.fitness)


np.save('zad4_po_p_mutation.npy', np.array(mutation_probabilities_best_fitnesses).reshape(4, 10))