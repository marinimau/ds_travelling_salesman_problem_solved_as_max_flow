"""
Copyright (c) 2021 Mauro Marini

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation
files (the "Software"), to deal in the Software without
restriction, including without limitation the rights to use,
copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following
conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
"""


import numpy as np

from conf import loading_params


def load_costs_matrix(filename):
    """
    Load the costs matrix given the filename
    :param filename: a string containing the name of the file
    :return: the coast matrix
    """
    costs = []
    read = False
    f = open(filename, "r")
    for line in f:
        # Skip last line
        if "];" in line:
            read = False
        # Read row, replace wrong character and convert into float list
        if read:
            row = line.replace('[', '')
            row = row.replace('],', '')
            row = row.replace(']', '')
            row = row.split(',')
            row = [float(x) for x in row]
            costs.append(row)
        # Start reading values
        if "C = [" in line:
            read = True
    return transform_to_symmetric(costs) if loading_params['symmetric_costs'] else costs


def transform_to_symmetric(costs):
    """
    Make matrix costs symmetric
    :param costs: the cost matrix
    :return: the symmetric cost matrix
    """
    costs = np.matrix(costs).astype(int)
    if loading_params['maintain_maximum_cost']:
        costs = np.maximum(costs, costs.transpose())
    else:
        np.minimum(costs, costs.transpose())
    return costs.tolist()
