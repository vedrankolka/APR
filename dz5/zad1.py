from main import *
# calculate real values
real_xs = [x0]
ts = np.arange(start, end + step, step)

for t in ts[1:]:
    next_x1 = x0[0] * math.cos(t) + x0[1] * math.sin(t)
    next_x2 = x0[1] * math.cos(t) - x0[0] * math.sin(t)
    real_xs.append([next_x1, next_x2])

real_xs = np.array(real_xs)
if args.plot is True:
    plt.plot(ts, real_xs[:, 0])
    plt.plot(ts, real_xs[:, 1])
    plt.title("Real values")
    plt.show()

integrate(EulerIntegrator(A, B, step=step), x0, start, end, title="Euler", real_values=real_xs)
integrate(ReversedEulerIntegrator(A, B, step=step), x0, start, end, title="Reversed Euler", real_values=real_xs)
integrate(TrapezeIntegrator(A, B, step=step), x0, start, end, title="Trapeze", real_values=real_xs)
integrate(RungeKutta4Real(A, B, step=step), x0, start, end, title="Runge-Kutta 4 real", real_values=real_xs)

trapezeIntegrator = TrapezeIntegrator(A, B, step=step)
eulerIntegrator = EulerIntegrator(A, B, step=step)
reverseEulerIntegrator = ReversedEulerIntegrator(A, B, step=step)

integrate(PECEIntegrator(eulerIntegrator, reverseEulerIntegrator, 2), x0, start, end,
          title="PE(CE)^2 Euler-ReversedEuler", real_values=real_xs)

integrate(PECEIntegrator(eulerIntegrator, trapezeIntegrator, 1), x0, start, end,
          title="PECE Euler-Trapeze (aka Heune)", real_values=real_xs)
