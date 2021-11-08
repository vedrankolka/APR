import numpy as np
from opty import funky

from opty.funky import DerivableFunction


def find_unimodal_range(x0, h, f):
    l = x0 - h
    r = x0 + h
    m = x0
    step = 1

    fm = f(x0)
    fl = f(l)
    fr = f(r)

    if fl > fm and fm < fr:
        return l, r

    elif fm > fr:
        while True:
            l = m
            m = r
            fm = fr
            step *= 2
            r = x0 + h * step
            fr = f(r)

            if fm <= fr:
                break
    else:
        while True:
            r = m
            m = l
            fm = fl
            step *= 2
            l = x0 - h * step
            fl = f(l)

            if fm <= fl:
                break

    return l, r


def golden_ratio_search(f, a, b=None, e=1e-6, verbose=True):
    if b is None:
        a, b = find_unimodal_range(a, 1, f)

    k = 0.5 * (np.sqrt(5) - 1)
    c = b - k * (b - a)
    d = a + k * (b - a)
    fc = f(c)
    fd = f(d)

    while b - a > e:
        # kontrolni ispis
        if verbose is True:
            print(f'a={a} f(a)={f(a)} b={b} f(b)={f(b)} c={c} f(c)={f(c)} d={d} f(d)={f(d)}')

        if fc < fd:
            b = d
            d = c
            c = b - k * (b - a)
            fd = fc
            fc = f(c)
        else:
            a = c
            c = d
            d = a + k * (b - a)
            fc = fd
            fd = f(d)

    return a, b


def e_i(n, i):
    ei = np.zeros(n)
    ei[i] = 1.0
    return ei


def vectorize(x0):
    if isinstance(x0, float):
        return np.array([x0])
    else:
        return x0


def coord_axes_search(x0, f, e=1e-9, verbose=True):
    x0 = vectorize(x0)
    x = x0
    n = len(x0)
    while True:
        xs = np.array(x)
        for i in range(n):
            ei = e_i(n, i)
            f_lamda = lambda lamda: f(x + lamda * ei)
            a, b = golden_ratio_search(f_lamda, 1, verbose=verbose)
            x += (a + b) / 2.0 * ei
        diff = np.linalg.norm(x - xs, ord=2)
        if diff <= e:
            break

    return x


def calculate_simplex(x0, step):
    n = len(x0)
    X = [x0]

    for i in range(n):
        X.append(x0 + e_i(n, i) * step)

    return X


def find_min_index(arr, f=lambda x: x):
    index_of_min = 0
    for i in range(1, len(arr)):
        if f(arr[i]) < f(arr[index_of_min]):
            index_of_min = i

    return index_of_min


def simplex_nelder_mead(f, x0, step=1, alpha=1, beta=0.5, gamma=2, sigma=0.5, e=1e-6, verbose=True, callbacks=[]):
    x0 = vectorize(x0)
    X = calculate_simplex(x0, step)
    assert len(X) == len(x0) + 1  # TODO maknut ovo
    n = len(x0)
    f_negative = lambda x: -f(x)
    while True:
        h = find_min_index(X, f=f_negative)
        l = find_min_index(X, f=f)
        xc = 1 / n * sum([X[i] for i in range(n + 1) if i != h])
        # kontrolni ispis
        if verbose is True:
            print(f'xc={xc} f(xc)={f(xc)}')

        xr = (1 + alpha) * xc - alpha * X[h]
        if f(xr) < f(X[l]):
            xe = (1 - gamma) * xc - gamma * xr  # expansion(x)
            if f(xe) < f(X[l]):
                X[h] = xe
            else:
                X[h] = xr
        else:
            if all(f(xr) > f(X[j]) for j in range(n + 1) if j != h):
                if f(xr) < f(X[h]):
                    X[h] = xr
                xk = (1 - beta) * xc + beta * X[h]
                if f(xk) < f(X[h]):
                    X[h] = xk
                else:
                    # samo zapamtimo kopiju
                    X_l = 1.0 * X[l]
                    X = [sigma * (X[i] + X_l) for i in range(n + 1)]
            else:
                X[h] = xr

        div = 1 / n * sum([(f(X[i]) - f(xc)) ** 2 for i in range(n + 1)])
        if np.sqrt(div) <= e:
            break

        for callback in callbacks:
            callback(f, xc)

    return xc


def __search(f, xp, dx, n):
    x = xp * 1.0
    for i in range(n):
        P = f(x)
        x[i] += dx[i]
        N = f(x)
        if N > P:
            x[i] -= 2 * dx[i]
            N = f(x)
            if N > P:
                x[i] += dx[i]

    return x


def hook_jeeves_search(f, x0, dx=0.5, e=1e-6, verbose=True, callbacks=[]):
    x0 = vectorize(x0)
    xp = x0
    xb = x0
    n = len(x0)
    # ako su ostali default dx i e, proširit ih u vektore
    if isinstance(dx, float):
        dx = dx * np.ones(n)
    if isinstance(e, float):
        e = e * np.ones(n)
    while True:
        xn = __search(f, xp, dx, n)
        # kontrolni ispis
        if verbose is True:
            print(f'xb={xb} f(xb)={f(xb)} xp={xp} f(xp)={f(xp)} xn={xn} f(xn)={f(xn)}')
        if f(xn) < f(xb):
            xp = 2 * xn - xb
            xb = xn
        else:
            dx /= 2
            xp = xb

        if all([dx[i] <= e[i] for i in range(n)]):
            break

        for callback in callbacks:
            callback(f, xb)

    return xb


def stohastic_gradient_descent(f: DerivableFunction, x0, line_search=False, e=1e-6, verbose=False, patience=5):
    x = np.array(x0)
    f_old = f(x)
    not_better_counter = 0

    while True:
        gradient = f.gradient(x)
        if any(np.isnan(gradient)) or any(np.isinf(gradient)):
            print('Gradient diverged frfr. x =', x)
            return None

        # if the gradient is very smoll, done
        if np.linalg.norm(gradient, ord=2) <= e:
            break

        if line_search:
            a, b = golden_ratio_search(lambda lamda: f(x + lamda * gradient), 1, verbose=verbose)
            delta_x = (a + b) / 2.0 * gradient
        else:
            delta_x = -gradient

        x += delta_x
        f_new = f(x)

        if f_new >= f_old:
            not_better_counter += 1
            if not_better_counter > patience:
                print('Gradient did not converge.')
                return None
        else:
            not_better_counter = 0

        f_old = f_new

    return x


def newton_raphson(f: DerivableFunction, x0, line_search=False, e=1e-6, verbose=False, patience=5):
    x = np.array(x0)
    f_old = f(x)
    not_better_counter = 0

    while True:
        gradient = f.gradient(x)
        hessian = f.hessian(x)

        if any(np.isnan(gradient)) or any(np.isinf(gradient)):
            print('Gradient diverged frfr. x =', x)
            return None

        if any([any(np.isnan(line)) for line in hessian]) or any([any(np.isinf(line)) for line in hessian]):
            print('Hessian diverged frfr. x =', x)
            return None

        # if the gradient is very smoll, done
        if np.linalg.norm(gradient, ord=2) <= e:
            break

        hessian_inv = np.linalg.inv(hessian)

        if line_search:
            a, b = golden_ratio_search(lambda lamda: f(x + lamda * hessian_inv @ gradient), 1, verbose=verbose)
            delta_x = (a + b) / 2.0 * hessian_inv @ gradient
        else:
            delta_x = - hessian_inv @ gradient

        x += delta_x
        f_new = f(x)

        if f_new >= f_old:
            not_better_counter += 1
            if not_better_counter > patience:
                print('Gradient did not converge.')
                return None
        else:
            not_better_counter = 0

        f_old = f_new

    return x


def box_algorithm(f, x0, explicit_constraint, inequality_constraints=[], e=1e-6, alpha=1.3, patience=1000):
    x0 = np.array(x0)
    xmin = explicit_constraint.xmin * np.ones(len(x0)) + e
    xmax = explicit_constraint.xmax * np.ones(len(x0)) - e
    if not explicit_constraint(x0) or not all(ic(x0) >= 0 for ic in inequality_constraints):
        print('x0 no good.')
        return None

    xc = x0
    X = []
    for i in range(2 * len(x0)):
        x_new = xmin + np.random.uniform(0, 1, len(xc)) * (xmax - xmin)

        counter = 0
        while any(ic(x_new) < 0 for ic in inequality_constraints):
            x_new = 0.5 * (x_new + xc)
            counter += 1
            if counter > patience:
                print('Damn. We givin up.')
                return None

        X.append(x_new)
        xc = sum(X) / len(X)

    not_better_counter = 0
    f_xc_old = f(xc)
    while True:
        X.sort(key=lambda x: f(x))
        h = -1
        h2 = -2
        xc = sum(X[:-1]) / (len(X) - 1)
        # check if the algorithm made improvents
        f_xc_new = f(xc)
        if f_xc_new > f_xc_old - e: # znaci ak nije bar za e bolji
            not_better_counter += 1
            if not_better_counter > patience:
                print('Did not converge.')
                return None
        else:
            not_better_counter = 0
            f_xc_old = f_xc_new

        xr = (1 + alpha) * xc - alpha * X[h]

        xr[xr < xmin] = xmin[xr < xmin]
        xr[xr > xmax] = xmax[xr > xmax]

        counter = 0
        while any(ic(xr) < 0 for ic in inequality_constraints):
            xr = 0.5 * (xr + xc)
            counter += 1
            if counter > patience:
                print('Damn! We givin up!')
                return None

        if f(xr) > f(X[h2]):
            xr = 0.5 * (xr + xc)

        X[h] = xr

        # uvjet zaustavljanja
        div = 1 / len(X) * sum([(f(x) - f(xc)) ** 2 for x in X])
        if np.sqrt(div) <= e:
            break

    return X[find_min_index(X, f)]


def create_contraints_function(inequality_constraints):
    def G(x):
        sum = 0.0
        for ic in inequality_constraints:
            value = ic(x)
            if value < 0:
                sum -= value
        return sum

    return G


def contsrained_simplex_nelder_mead(f, x0, inequality_constraints=[], equality_constraints=[], e=1e-6, alpha=1.3,
                                    patience=1000):
    x0 = np.array(x0)
    if not all(ic(x0) >= 0 for ic in inequality_constraints):
        print('Finding valid x0...')
        # TODO impl equality constraints
        x0 = hook_jeeves_search(create_contraints_function(inequality_constraints), x0, verbose=False)

    if not all(ic(x0) >= 0 for ic in inequality_constraints):
        print('Search failed.')
        return None

    print('x0 =', x0)

    transformed_function = funky.TransformedFunction(f, inequality_constraints, equality_constraints)

    def callback(function, x):
        if function.t < 1e12:
            function.t *= 10

    x = hook_jeeves_search(transformed_function, x0, verbose=False, callbacks=[callback])
    return x
