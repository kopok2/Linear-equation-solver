# coding=utf-8
"""LU decomposition module.

Module for lower-upper factorization of matrix using Doolittle algorithm.
"""

import numpy as np
from fractions import Fraction
from random import randrange


class DecompositionError(Exception):
    """Signals problems with matrix factorization.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


def lu_decomposition(matrix, silent=True):
    """Factors matrix into a lower triangular matrix and an upper triangular matrix.

    Args:
        matrix: numpy double subscriptable square object.
        silent: whether to display factorization steps (bool).

    Returns:
        Tuple (L, U):
            L - lower triangular matrix (1 on diagonal)
            U - upper triangular matrix
    """

    factored_matrix = np.array([[Fraction(y, 1) for y in x] for x in matrix])
    rank = factored_matrix[0].__len__()
    lower_matrix = np.array([[Fraction(1, 1) if x == y else Fraction() for x in range(rank)] for y in range(rank)])
    upper_matrix = np.array([[Fraction(1, 1) if x == y else Fraction() for x in range(rank)] for y in range(rank)])
    step_count = 0

    for i in range(rank):

        # calculating upper matrix
        for j in range(i, rank):
            sub_sum = 0
            formula = "u" + str(i + 1) + str(j + 1) + " = a" + str(i + 1) + str(j + 1)
            step_count += 1
            for k in range(i):
                sub_sum += lower_matrix[i][k] * upper_matrix[k][j]
                formula += " - " + "l" + str(i + 1) + str(k + 1) + "u" + str(k + 1) + str(j + 1)
            upper_matrix[i][j] = Fraction(factored_matrix[i][j] - sub_sum, 1)
            
            if not silent:
                print(str(step_count) + " / " + str(rank**2))
                print(step_count, formula, upper_matrix[i][j])

        # calculating lower matrix
        for j in range(i + 1, rank):
            if i != rank:
                sub_sum = 0
                formula = "l" + str(j + 1) + str(i + 1) + " = (a" + str(j + 1) + str(i + 1)
                step_count += 1
                for k in range(i):
                    sub_sum += lower_matrix[j][k] * upper_matrix[k][i]
                    formula += " - " + "l" + str(j + 1) + str(k + 1) + "u" + str(k + 1) + str(i + 1)
                try:
                    lower_matrix[j][i] = Fraction((factored_matrix[j][i] - sub_sum), upper_matrix[i][i])
                except ZeroDivisionError:
                    raise DecompositionError("Zero found in matrix.")
                formula += ") / u" + str(i + 1) + str(i + 1)
                
                if not silent:
                    print(str(step_count) + " / " + str(rank**2))
                    print(step_count, formula, lower_matrix[j][i])
    lower_counted = [[float(fraction) for fraction in row] for row in lower_matrix]
    upper_counted = [[float(fraction) for fraction in row] for row in upper_matrix]

    return lower_counted, upper_counted
