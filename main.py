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

import time

import conf
from maximum_flow import MaximumFlowSolver
from assignment import *
from load_dataset import *
from subpath_finder import get_paths
from utils import *

# Costs Matrix
costs = []

if __name__ == '__main__':
    costs = load_costs_matrix("dataset/basic.dat")
    # Number of nodes
    nodes = len(costs)
    # Range of the nodes
    range_nodes = range(nodes)
    MaximumFlowSolver.t_nodes = list(range_nodes)[5:]
    solved = False
    paths = None
    start = time.time()
    # Create the model
    m, x = create_assignment_model('tsp_continuous_relaxing', range_nodes, costs)
    while not solved:
        # Solve the model
        solution = m.solve()
        # Print the report
        m.report()
        # Get the solution as df
        df = solution.as_df()
        # Convert the dataframe
        df = convert_dataframe_names(df, nodes)
        # Get al the paths
        paths = get_paths(df, nodes)
        # Until there are no sub paths left
        if len(paths) != 1:
            if conf.VERBOSE:
                print('#paths: ' + str(len(paths)))
            # 1. Get capacities from continuous relaxing solution
            max_flow = MaximumFlowSolver(df, range_nodes, 0)
            # 2. Solve max flow using capacities
            solution = max_flow.solve_max_flow()
            # 3. Get constraint from max flow

            # 4. add constraint to initial problem
            break # remove this
    if paths is not None:
        # Get the final path
        path = convert_path_to_final(paths[0][0])
        # Convert the path to the decision variable matrix
        matrix = convert_path_to_matrix(path, nodes)
        # Convert the cost list of list to a numpy matrix
        costs_matrix = numpy.array(costs)
        # Multiply and sum the result
        result = matrix * costs_matrix
        end = time.time()
        elapsed = end - start
        if conf.VERBOSE:
            print('cost: ' + str(result.sum()) + '\telapsed time: ' + str(elapsed))
