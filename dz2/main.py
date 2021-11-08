#!/usr/bin/python3.7
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

print('-------------- ZAD 1 --------------')
x0 = conf['zad1'].getfloat('x0')
f = funky.Function3Translated()
f = funky.CacheFunctionProxy(f)

a, b = algy.golden_ratio_search(f, x0, e=e, verbose=verbose)
print(f'rjesenje = {(a+b)/2} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.coord_axes_search(x0, f, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.hook_jeeves_search(f, x0, dx, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

print('-------------- ZAD 2 --------------')
print('f1')
f = funky.CacheFunctionProxy(funky.Function1())
x0 = np.array([-1.9, 2])

x = algy.coord_axes_search(x0, f, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.hook_jeeves_search(f, x0, dx, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

print('f2')
f = funky.CacheFunctionProxy(funky.Function2())
x0 = np.array([0.1, 0.3])

x = algy.coord_axes_search(x0, f, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.hook_jeeves_search(f, x0, dx, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

print('f3')
f = funky.CacheFunctionProxy(funky.Function3())
x0 = np.array([3.0, 2.0, 5.0, 1.0, -2.0])

x = algy.coord_axes_search(x0, f, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

x = algy.hook_jeeves_search(f, x0, dx, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()}')
f.set_call_count(0)

print('f4')
f = funky.CacheFunctionProxy(funky.Function4())
x0 = np.array([0.0, 0.0])

x = algy.coord_axes_search(x0, f, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()} f(x)={f(x)}')
f.set_call_count(0)

x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()} f(x)={f(x)}')
f.set_call_count(0)

x = algy.hook_jeeves_search(f, x0, dx, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()} f(x)={f(x)}')
f.set_call_count(0)

print('-------------- ZAD 3 --------------')
x0 = np.array([5.0, 5.0])
f = funky.CacheFunctionProxy(funky.Function4())

x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()} f(x)={f(x)}')
f.set_call_count(0)

x = algy.hook_jeeves_search(f, x0, dx, e=e, verbose=verbose)
print(f'rjesenje = {x} broj poziva = {f.get_call_count()} f(x)={f(x)}')
f.set_call_count(0)

print('-------------- ZAD 4 --------------')
x0 = np.array([0.5, 0.5])
f = funky.CacheFunctionProxy(funky.Function1())

print("x0 = (0.5, 0.5)")
arr = []
for i in range(20):
    x = algy.simplex_nelder_mead(f, x0, i+1, alpha, beta, gamma, sigma, e, verbose=False)
    arr.append((f(x), f.get_call_count()))
    f.set_call_count(0)

for value, call_count in arr:
    print(value, call_count)

print("x0 = (20, 20)")
x0 = np.array([20.0, 20.0])
arr = []
for i in range(20):
    x = algy.simplex_nelder_mead(f, x0, i + 1, alpha, beta, gamma, sigma, e, verbose=False)
    arr.append((f(x), f.get_call_count()))
    f.set_call_count(0)

for value, call_count in arr:
    print(value, call_count)

print('-------------- ZAD 5 --------------')

f = funky.CacheFunctionProxy(funky.Function6())
solutions = []
for i in range(1000):
    x01 = random.uniform(-50, 50)
    x02 = random.uniform(-50, 50)
    x0 = np.array([x01, x02])
    x = algy.simplex_nelder_mead(f, x0, step, alpha, beta, gamma, sigma, e, verbose=False)
    solutions.append(x)

correct = sum([1 for x in solutions if f(x) <= 1e-3])
print(correct/len(solutions) * 100, '%')