from main import *

integrate(EulerIntegrator(A, B, step=step), x0, start, end, title="Euler")
integrate(ReversedEulerIntegrator(A, B, step=step), x0, start, end, title="Reversed Euler")
integrate(TrapezeIntegrator(A, B, step=step), x0, start, end, title="Trapeze")
integrate(RungeKutta4Real(A, B, step=step), x0, start, end, title="Runge-Kutta 4 real")

trapezeIntegrator = TrapezeIntegrator(A, B, step=step)
eulerIntegrator = EulerIntegrator(A, B, step=step)
reverseEulerIntegrator = ReversedEulerIntegrator(A, B, step=step)

integrate(PECEIntegrator(eulerIntegrator, reverseEulerIntegrator, 2), x0, start, end,
          title="PE(CE)^2 Euler-ReversedEuler")
integrate(PECEIntegrator(eulerIntegrator, trapezeIntegrator, 1), x0, start, end,
          title="PECE Euler-Trapeze (aka Heune)")
