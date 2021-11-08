#!/usr/bin/python3.8.5
from opty import algy, funky
import numpy as np
import sys
from configparser import ConfigParser
import random

conf = ConfigParser()
conf.read(sys.argv[1])

h = conf['GENERAL'].getfloat('h')
e = conf['GENERAL'].getfloat('e')
verbose = conf['GENERAL'].getboolean('verbose')
step = conf['simplex'].getfloat('step')
alpha = conf['simplex'].getfloat('alpha')
beta = conf['simplex'].getfloat('beta')
gamma = conf['simplex'].getfloat('gamma')
sigma = conf['simplex'].getfloat('sigma')
dx = np.fromstring(conf['hooke_jeeves'].get('dx'), sep=' ')
e_hj = np.fromstring(conf['hooke_jeeves'].get('e'), sep=' ')

if len(dx) == 1:
    dx = dx[0]

if len(e_hj) == 1:
    e_hj = e_hj[0]


def __format(x, f):
    if x is None:
        return 'No minimum found'

    return "x = {:4.3f} {:4.3f} f(x) = {:4.3f} cc = {:6d} gc = {:<4d} hc = {:<4d}".format(
        x[0], x[1], f(x), f.call_count, f.gradient_call_count, f.hessian_call_count)


# ZAD 1 ======================================================================
print('\n========== Stohastic gradient descent on f3 (zad 1) =============\n')

f3 = funky.F3()
x = algy.stohastic_gradient_descent(f3, np.array([0, 0]), line_search=False)
print(__format(x, f3))

f3 = funky.F3()
x = algy.stohastic_gradient_descent(f3, np.array([0.0, 0.0]), line_search=True)
print(__format(x, f3))
# ZAD 2 ======================================================================
print('\n=========== SGD and Newton-Raphson on f1 and f2(zad 2) ==========\n')

print("Rosenbrock's banana")
f1 = funky.RosenbrocksBanana()
print('SGD')
x = algy.stohastic_gradient_descent(f1, np.array([-1.9, 2.0]), line_search=True)
print(__format(x, f1))
f1 = funky.RosenbrocksBanana()
print('Newton-Raphson')
x = algy.newton_raphson(f1, np.array([-1.9, 2.0]), line_search=True)
print(__format(x, f1))

print('F2')
f2 = funky.F2()
print('SGD')
x = algy.stohastic_gradient_descent(f2, np.array([0.1, 0.3]), line_search=True)
print(__format(x, f2))
f2 = funky.F2()
print('Newton-Raphson')
x = algy.newton_raphson(f2, np.array([0.1, 0.3]), line_search=True)
print(__format(x, f2))
# ZAD 3 ======================================================================
print('\n========== Roddy Rich - The Box on f1 and f2 (zad 3) ============\n')

explicit_constraint = funky.ExplicitContraint(-100.0, 100.0)
inequality_constraints = [funky.g1, funky.g2]

print("Rosenbrock's banana")
f1 = funky.RosenbrocksBanana()
x = algy.box_algorithm(f1, np.array([-1.9, 2]), explicit_constraint, inequality_constraints)
print(__format(x, f1))

print('F2')
f2 = funky.F2()
x = algy.box_algorithm(f2, np.array([0.1, 0.3]), explicit_constraint, inequality_constraints)
print(__format(x, f2))

# ZAD 4 ======================================================================
print('\n=== Transformed simplex by Nelder & Mead on f1 and f2 (zad 4) ===\n')

print("Rosenbrock's banana")
f1 = funky.RosenbrocksBanana()
x = algy.contsrained_simplex_nelder_mead(f1, np.array([3.0, 7.0]), [funky.g1, funky.g2])
print(__format(x, f1))

print("F2")
f2 = funky.F2()
x = algy.contsrained_simplex_nelder_mead(f2, np.array([0.1, 0.3]), [funky.g1, funky.g2])
print(__format(x, f2))

# ZAD 5 ======================================================================
print('\n====== Transformed simplex by Nelder & Mead on f4 (zad 5) =======\n')
f4 = funky.F4()
x0 = np.array([5.0, 5.0])
inequality_constraints = [funky.g3, funky.g4]
equality_constraints = [funky.h1]
x = algy.contsrained_simplex_nelder_mead(f4, x0, inequality_constraints, equality_constraints)
print(__format(x, f4))
