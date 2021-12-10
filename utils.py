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

import numpy


def convert_row(d, nodes):
    """
    Convert a row of the column "name" of the dataframe. It computes the starting node and the ending node of an arc
    :param d: The row of the column name
    :param nodes: Number of nodes
    :return: The row and column (start and end) values
    """
    row = int(int(d['name'][1:]) / nodes) + 1
    col = int(int(d['name'][1:]) % nodes)
    if col == 0:
        col = nodes
        row = row - 1
    return row, col


def convert_dataframe_names(df, nodes):
    """
    Convert the values of the column names with a field start (the starting node of the arc) and a field end
    (the ending node of the arc)
    :param df: a Pandas dataframe that contains the solution of the model
    :param nodes: the number of nodes
    :return: a Pandas dataframe with three fields [value, start, end]
    """
    start = []
    end = []
    for index, d in df.iterrows():
        pos = convert_row(d, nodes)
        start.append(pos[0] - 1)
        end.append(pos[1] - 1)
    df.drop('name', axis=1, inplace=True)
    df['start'] = start
    df['end'] = end
    return df


def solution_to_matrix(df, nodes):
    """
    Get the decision variable x in matrix form
    :param df: a Pandas dataframe that contains the solution of the model
    :param nodes: the number of nodes
    :return: the matrix that contains the solution
    """
    matrix = numpy.zeros((nodes, nodes))
    for index, d in df.iterrows():
        pos = convert_row(d, nodes)
        row = pos[0] - 1
        col = pos[1] - 1
        matrix[row][col] = 1
    return matrix


def convert_path_to_matrix(path, nodes):
    """
    Convert the path to the decision variable matrix x
    :param path: the path list
    :param nodes: the number of nodes
    :return: A boolean numpy matrix with the decision variable x
    """
    matrix = numpy.zeros((nodes, nodes))
    for i in range(len(path) - 1):
        matrix[path[i]][path[i + 1]] = 1
    return matrix


def convert_path_to_final(path):
    """
    Split the path to get the final path form (starts from node 0 and end to node 0
    :param path: The path list
    :return: A list with the path in final form
    """
    p1, p2 = split_path(path, 0)
    p2 = [0] + p2
    return p2 + p1


def split_path(path, val):
    """
    Split the path when it encounter a certain value
    :param path: the path list
    :param val: the value
    :return: two sub paths -> sub_path1 from start to value / sub_path2 form after the value to the end
    """
    sub_path1 = []
    sub_path2 = path[:-1]
    for i in path:
        sub_path1.append(i)
        sub_path2.remove(i)
        if i == val:
            break
    return sub_path1, sub_path2


def find_path_by_node(paths, node):
    """
    Find a path by node
    :param paths: the path list
    :param node: the given node
    :return: the path of the node
    """
    for i in range(len(paths)):
        nodes = paths[i][0]
        for n in nodes:
            if n == node:
                return nodes
    return None

