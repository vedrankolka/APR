import numpy as np
import argparse
import math
import matplotlib.pyplot as plt

from integrators.integrators import (
    Integrator,
    EulerIntegrator,
    ReversedEulerIntegrator,
    TrapezeIntegrator,
    RungeKutta4Real,
    PECEIntegrator,
)

parser = argparse.ArgumentParser()

parser.add_argument("A", help="Path to matrix A in system: dx/dt = A * x + B * r(t)")
parser.add_argument("B", help="Path to matrix B in system: dx/dt = A * x + B * r(t)")
parser.add_argument("x0", help="Path to x(t=0) in system: dx/dt = A * x + B * r(t)")
parser.add_argument("-v", "--verbose", help="period of printing variables; default is 100", type=int)
parser.add_argument("-T", "--step", help="period of integration; default is 0.01", type=float, default=0.01)
parser.add_argument("-t0", "--start", help="start of integration; default is 0", type=float, default=0)
parser.add_argument("-t1", "--end", help="end of integration; default is 10", type=float, default=10)
parser.add_argument("-s", "--save", help="file to which the results should be saved", type=str)
parser.add_argument("-p", "--plot", action="store_true", default=False)

args = parser.parse_args()

v = args.verbose
step = args.step
start = args.start
end = args.end


def print_callback(x):
    print(f"x = {x}")


def parse_matrix(lines):
    arr = []
    for line in lines:
        line = line.strip()
        numbers = [float(n) for n in line.split(' ')]
        arr.append(numbers)

    return np.array(arr)


def integrate(integrator: Integrator, x_start, start, end, title=None, real_values=None):
    xs, ts = integrator.integrate(x_start, start, end, callbacks=[print_callback], v=v)

    if args.plot is True:
        x1s = xs[:, 0]
        x2s = xs[:, 1]
        plt.plot(ts, x1s)
        plt.plot(ts, x2s)
        plt.title(title)
        plt.show()

    if args.save is not None:
        np.save(args.save, xs)

    if real_values is not None:
        error = np.sum(np.abs(real_values - xs))
        print("sum of absolute errors: {:.8} ({})".format(error, title))


with open(args.A, 'r', encoding='utf8') as a_file:
    A = parse_matrix(a_file)

with open(args.B, 'r', encoding='utf8') as b_file:
    B = parse_matrix(b_file)

with open(args.x0, 'r', encoding='utf8') as x0_file:
    x0 = parse_matrix(x0_file)
