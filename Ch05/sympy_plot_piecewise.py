import numpy as np
import numpy.linalg as na
import matplotlib.pyplot as plt
import scipy.integrate as si
import sympy as sy
import sympy.plotting as splot
import IPython.display as disp


def plot_numpy():
    x = sy.Symbol('x', real=True)
    y = sy.Piecewise((- x, x < 0), (x, x >= 0))

    splot.plot(y, (x, -5, 5))


if __name__ == '__main__':
    plot_numpy()
