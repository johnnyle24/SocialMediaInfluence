import sys
import time
from nxmetis import partition

from load import load_networkx_graph, load_snap_graph
from influence import set_influence


def max_influence_set(network, k):
    max_set = []

    # Partition the graph
    _, part = partition(network, k)

    # Get the highest degree node in each partition
    for i in range(k):
        graph = network.subgraph(part[i])
        max_node, max_degree = max(graph.degree, key=lambda pair: pair[1])
        max_set.append(max_node)

    return max_set


if __name__ == '__main__':
    # Parameters
    k = int(sys.argv[1])

    # Load the graphs
    snap_graph = load_snap_graph('../data/wiki-Vote.txt')
    networkx_graph = load_networkx_graph('../data/wiki-Vote.txt')

    # Partition the graph
    start = time.time()
    max_set = max_influence_set(networkx_graph, k)
    end = time.time()

    # Show the influence
    influence = set_influence(snap_graph, max_set)

    print('time to find set: ' + str(end - start))
    print('set influence:    ' + str(influence) + '\n')
