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


def get_subsequent_node(visited):
    """
    get the subsequent node
    :param visited: a boolean list tracking the nodes which have been visited
    :return: -1 if all nodes have been visited or the index of the first node that hasn't been visited
    """
    for idx, val in enumerate(visited):
        if not val:
            return idx
    return -1


def get_paths(df, nodes):
    """
    return all the sub paths
    :param df: a Pandas dataframe that contains the solution of the model
    :param nodes: the number of the nodes
    :return: a list of sub paths (list of list)
    """
    visited = [False] * nodes
    paths = []
    path = []
    node_counter = 0
    # Set the node 1 to visited and add it to the path
    visited[df['start'].iloc[0]] = True
    path.append(df['start'].iloc[0])
    node_counter += 1
    # Take the endpoint of the arc
    subsequent = df['end'].iloc[0]
    while subsequent != -1:
        # Set the start node to the visited and add it to the path
        visited[df['start'].iloc[subsequent]] = True
        path.append(df['start'].iloc[subsequent])
        node_counter += 1
        # If the end of the arc is not visited
        if not visited[df['end'].iloc[subsequent]]:
            # Change the subsequent node with the end of the arc
            subsequent = df['end'].iloc[subsequent]
        # If the end of the arc is visited
        else:
            # Add the end node to the path
            path.append(df['end'].iloc[subsequent])
            # Add the sub path to the paths list
            paths.append((path, node_counter))
            # Start a new path
            path = []
            node_counter = 0
            # Get the subsequent node not visited
            subsequent = get_subsequent_node(visited)
    return paths
