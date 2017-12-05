import sys
import time
from nxmetis import partition

from load import load_networkx_graph, load_snap_graph
from influence import set_influence


def max_influence_set(k, networkx_graph):
    S = []

    # Partition the graph
    _, part = partition(networkx_graph, k)

    # Get the highest degree node in each partition
    for i in range(k):
        graph = networkx_graph.subgraph(part[i])
        max_node, max_degree = max(graph.degree, key=lambda pair: pair[1])
        S.append(max_node)

    return S


if __name__ == '__main__':
    # Parameters
    k = int(sys.argv[1])

    # Load the graphs
    networkx_graph = load_networkx_graph('../data/wiki-Vote.txt')
    snap_graph = load_snap_graph('../data/wiki-Vote.txt')

    # Partition the graph
    start = time.time()
    S = max_influence_set(k, networkx_graph)
    end = time.time()
    print('Time to find set: ' + str(end - start))

    # Show the influence
    influence = set_influence(S, snap_graph)
    print('Influence:        ' + str(influence))
