from main import *

r = lambda t: t

integrate(EulerIntegrator(A, B, step=step, r=r), x0, start, end, title="Euler")
integrate(ReversedEulerIntegrator(A, B, step=step, r=r), x0, start, end, title="Reversed Euler")
integrate(TrapezeIntegrator(A, B, step=step, r=r), x0, start, end, title="Trapeze")
integrate(RungeKutta4Real(A, B, step=step, r=r), x0, start, end, title="Runge-Kutta 4 real")

trapezeIntegrator = TrapezeIntegrator(A, B, step=step, r=r)
eulerIntegrator = EulerIntegrator(A, B, step=step, r=r)
reverseEulerIntegrator = ReversedEulerIntegrator(A, B, step=step, r=r)

integrate(PECEIntegrator(eulerIntegrator, reverseEulerIntegrator, 2), x0, start, end,
          title="PE(CE)^2 Euler-ReversedEuler")
integrate(PECEIntegrator(eulerIntegrator, trapezeIntegrator, 1), x0, start, end,
          title="PECE Euler-Trapeze (aka Heune)")
