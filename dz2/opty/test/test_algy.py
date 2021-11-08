from opty import algy

def my_test_unimodal_quadratic_from_gl(gl):
    f = lambda x: (x - 2) ** 2 + 1
    h = 1
    l, r = algy.find_unimodal_range(gl, h, f)
    assert l <= 2
    assert r >= 2


def test_find_unimodal_range():
    # find from right
    my_test_unimodal_quadratic_from_gl(8)
    # find from right
    my_test_unimodal_quadratic_from_gl(-3)
    # find from first try
    my_test_unimodal_quadratic_from_gl(2.1)


def my_test_quadratic_golden_ratio_from_x0(x0):
    e = 1e-6
    xmin = 2
    f = lambda x: (x - 2) ** 2 + 1

    a, b = algy.golden_ratio_search(f, x0, e=e)
    assert xmin - a <= e
    assert b - xmin <= e


def test_golden_radio_search():
    my_test_quadratic_golden_ratio_from_x0(-3)
    my_test_quadratic_golden_ratio_from_x0(0)
    my_test_quadratic_golden_ratio_from_x0(2)
    my_test_quadratic_golden_ratio_from_x0(2.1)
    my_test_quadratic_golden_ratio_from_x0(4)
    my_test_quadratic_golden_ratio_from_x0(8)


def test_coord_axes_search():
    assert 1 == 1
