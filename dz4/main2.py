from ga.functions import *
from ga.population.crossing import GaussCrossing, BLXalphaCrossing, UniformCrossing, OnePointCrossing
from ga.population.mutation import OneBitMutation, DoubleGaussMutation
from ga.solutions import DoubleArraySolution, BitArraySolution

lower = np.array([-5, -5, 0, 0])
upper = np.array([5, 5, 1, 1])

momma = DoubleArraySolution(4, lower, upper, arr=np.array([-5, -5, 0.6, 0.8]))
poppa = DoubleArraySolution(4, lower, upper, arr=np.array([5, 0, 1.0, 0.9]))

gauss_crossing = GaussCrossing()
for i in range(10):
    print(gauss_crossing.cross(momma, poppa))

print('-'*20)

blx_alpha_crossing = BLXalphaCrossing(0.2)
for i in range(10):
    print(blx_alpha_crossing.cross(momma, poppa))

print('-'*50)

blx_alpha_crossing = BLXalphaCrossing(np.array([0.5, 0.5, 0, 0]))
for i in range(10):
    print(blx_alpha_crossing.cross(momma, poppa))

momma = BitArraySolution(n_variables=6, e=1.0, arr=np.array([1, 0, 1, 1, 1, 0], np.bool))
poppa = BitArraySolution(n_variables=6, e=1.0, arr=np.array([0, 1, 0, 1, 0, 1], np.bool))

uniform_crossing = UniformCrossing()

for i in range(10):
    print(uniform_crossing.cross(momma, poppa))

one_point_crossing = OnePointCrossing()
for i in range(10):
    print(one_point_crossing.cross(momma, poppa))

print(momma.fitness)

mutation = OneBitMutation(0.5, 0.1)
solution = BitArraySolution(1, e=0.01)
mutation.mutate_population([solution, solution, solution])

mutation = DoubleGaussMutation(0.99, 0.5, 1)
solution = DoubleArraySolution(5, upper=5)
mutation.mutate_solution(solution)
print(solution)

f1 = RosenbrocksBanana()
f2 = Function3()
f3 = SchaffersFunction()
f4 = AlmostSchaffers()

x1 = np.array([1.0, 1.0])
x2 = np.array([1.0, 2.0])
x3 = np.array([0.0, 0.0])
x4 = np.array([0.0, 0.0])

print(f1(x1))
print(f2(x2))
print(f3(x3))
print(f4(x4))
