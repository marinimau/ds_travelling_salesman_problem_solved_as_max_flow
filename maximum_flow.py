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

from docloud.status import JobSolveStatus
from docplex.mp.model import Model

import conf
from utils import find_path_by_node


class MaximumFlowSolver:
    """
    Maximum Flow solver
    """

    t_nodes = []

    def __init__(self, solution_df, range_nodes, s=0,):
        """
        Constructor
        :param solution_df: the solution of the continuous relaxation (pd dataframe)
        :param range_nodes: an iterator from 0 to #nodes-1
        :param s: the starting node
        """
        assert len(MaximumFlowSolver.t_nodes) > 0
        self.__s = s
        self.__t = MaximumFlowSolver.t_nodes.pop(0)
        self.__crate_max_flow_model(range_nodes)
        self.__set_transhipment_for_all_nodes(range_nodes)
        self.__set_capacity_constraints(range_nodes, solution_df)
        self.__create_objective_function()

    def __set_capacity_constraints(self, range_nodes, solution_df):
        """
        Set capacity for each edge
        :param range_nodes:  an iterator from 0 to #nodes-1
        :param solution_df:  the solution of the continuous relaxation (pd dataframe)
        :return:
        """
        for i in range_nodes:
            for j in range_nodes:
                value = max(self.__get_capacity_constraint(i, j, solution_df),
                            self.__get_capacity_constraint(j, i, solution_df))
                if conf.VERBOSE:
                    print('start: ' + str(i) + ', end: ' + str(j) + ', value: ' + str(value))
                self.__model.add_constraint(self.__x[i, j] <= value)
                self.__model.add_constraint(self.__x[j, i] <= value)

    @staticmethod
    def __get_capacity_constraint(start, end, solution_df):
        """
        Get capacities from the continuous relaxation solution and set it as constraints of the current model
        :param start: the start node
        :param end: the end node
        :param solution_df: the solution of the continuous relaxation (pd dataframe)
        :return: the value for capacity
        """
        value = solution_df.loc[(solution_df['start'] == start) & (solution_df['end'] == end)]['value'].tolist()
        value.append(0.5)
        return value[0]

    def __set_transhipment_for_all_nodes(self, range_nodes):
        """
        Set b(v) = 0 for all v in V
        :param range_nodes: an iterator from 0 to #nodes-1
        :return:
        """
        [self.__model.add_constraint(self.__model.sum([
            - (self.__model.sum(self.__x[j, i] if i != j else 0 for j in range_nodes)),
            self.__model.sum(self.__x[i, j] if i != j else 0 for j in range_nodes)
        ]) == 0) for i in range_nodes]
        [self.__model.add_constraint(self.__x[i, i] == 0) for i in range_nodes]

    def __crate_max_flow_model(self, range_nodes):
        """
        Create max flow model
        :param range_nodes: an iterator from 0 to #nodes-1
        :return:
        """
        self.__model = Model(name='max_flow_from_' + str(self.__s) + '_to_' + str(self.__t), log_output=conf.VERBOSE)
        self.__x = self.__model.continuous_var_matrix(range_nodes, range_nodes)
        if conf.VERBOSE:
            print(self.__model.name + '\ts: ' + str(self.__s) + '\tt: ' + str(self.__t))

    def __create_objective_function(self):
        """
        create objective function
        :return:
        """
        self.__model.maximize(1 * self.__x[self.__t, self.__s])

    def solve_max_flow(self):
        """
        Solve max flow
        :return: the solution of the max flow problem
        """
        solution = self.__model.solve()
        if conf.VERBOSE:
            self.__model.report()
        MaximumFlowSolver.t_nodes.append(self.__t)
        return solution

    def export_constraint(self):
        """
        Export constraint generated by max flow
        :return: a tuple s, t
        """

        if conf.VERBOSE:
            print(self.__model.solve_status)
        if self.__model.solve_status == JobSolveStatus.INFEASIBLE_OR_UNBOUNDED_SOLUTION:
            raise Exception("INFEASIBLE_OR_UNBOUNDED_SOLUTION")
        else:
            if self.__model.solution.objective_value < 1:
                return self.__s, self.__t
            else:
                print('s: ' + str(self.__s) + ', t: ' + str(self.__t) + ', solution: ' + str(self.__model.solution.objective_value))
        if self.__model.solution.objective_value >= 1:
            print('s: ' + str(self.__s) + ', t: ' + str(self.__t) + ', solution: ' + str(self.__model.solution.objective_value < 1))
        return None, None

    def export_constraint_easy(self, paths):
        """
        Export constraint easy
        :return: a tuple s, t
        """
        p1 = find_path_by_node(paths, self.__s)
        p2 = find_path_by_node(paths, self.__t)
        if p1 != p2:
            return self.__s, self.__t
        return None, None
