"""System of linear equations solver module."""

import json
import random
import numpy as np
from fractions import Fraction
from lu_decomposer import lu_decomposition

def floatize_fractions1d(vector):
    return [float(x) for x in vector]


def floatize_fractions2d(matrix):
    return [[float(x) for x in row]for row in matrix]

    
def defloatize_fractions1d(vector):
    return [Fraction(x) for x in vector]


def defloatize_fractions2d(matrix):
    return [[Fraction(x) for x in row]for row in matrix]


def forward_substitution(variable_matrix, result_vector):
    result = []
    for x in range(result_vector.__len__()):
        sum = 0
        for y in range(x):
            sum += variable_matrix[x][y]*result[y]
        result.append((result_vector[x] - sum) / variable_matrix[x][x])
    return result


def backward_substitution(variable_matrix, result_vector):
    new_matrix = []
    new_results = []
    for row_id in range(variable_matrix.__len__()):
        new_matrix.append(variable_matrix[variable_matrix.__len__()- 1 - row_id][::-1])
        new_results.append(result_vector[variable_matrix.__len__()- 1 - row_id])
    return forward_substitution(new_matrix, new_results)[::-1]


class Equation:
    def __init__(self, variable_matrix=[[1]], result_vector=[[1]]):
        self.variable_matrix = variable_matrix
        self.result_vector = result_vector

    def __str__(self):
        results = self.solve()
        to_print = 'System of linear equations:\n\n'
        for x in range(self.variable_matrix.__len__()):
            first = True
            for y in range(self.variable_matrix.__len__()):
                if (not first) and (self.variable_matrix[x][y] >= 0):
                    to_print += "+"
                to_print += str(self.variable_matrix[x][y]) + "x" + str(y+1) + " "
                first = False
            to_print += "= " + str(self.result_vector[x]) + "\n"
        to_print += "\nResults:\n\n"
        for x in range(results.__len__()):
            to_print += "x" + str(x + 1) + " = " + str(results[x]) + "\n"
        return to_print

    def load_from_string(self, source):
        lines = source.split("\n")
        lines = list(filter(None, lines))
        size = lines.__len__()
        variable_matrix = []
        result_vector = []
        for line in lines:
            local_vars = [0 for x in range(size)]
            parts = line.split("=")
            result_vector.append(Fraction(float(parts[1])))
            for part in parts[0].split(" "):
                if part:
                    t = part.split("x")
                    x_id = int(t[1]) - 1
                    if not t[0]:
                        t[0] = 1
                    x_val = Fraction(float(t[0]))
                    local_vars[x_id] = x_val
            variable_matrix.append(local_vars)
        self.variable_matrix = variable_matrix
        self.result_vector = result_vector
            
    def save_to_file(self, path):
        out_dict = {'Matrix': floatize_fractions2d(self.variable_matrix), 
                    'Result': floatize_fractions1d(self.result_vector),
                    'XVector': floatize_fractions1d(self.solve())}
        with open(path, 'w') as outfile:
            json.dump(out_dict, outfile, indent=2)

    def load_from_file(self, path):
        with open(path, "r") as json_file:
            data = json.load(json_file)
            self.variable_matrix = defloatize_fractions2d(data['Matrix'])
            self.result_vector = defloatize_fractions1d(data['Result'])

    def generate_random(self, size=8, lowerlimit=-50 ,upperlimit=50):
        self.variable_matrix = [[random.randint(lowerlimit,upperlimit) for x in range(size)] for y in range(size)]
        self.result_vector = [random.randint(lowerlimit,upperlimit) for x in range(size)]

    def solve(self):
        factorized = lu_decomposition(self.variable_matrix)
        z = forward_substitution(factorized[0], self.result_vector)
        return backward_substitution(factorized[1], z)
