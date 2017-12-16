import sys
import time
from nxmetis import partition

from load import load_networkx_graph, load_snap_graph
from influence2 import set_influence


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

    # Measure the time
    start = time.time()

    # Partition for each k and compute the best set
    for i in range(1, k + 1):
        
        influence_total = 0

        for j in range(10):

            max_set = max_influence_set(networkx_graph, i)

            # Show the influence
            influence = set_influence(snap_graph, max_set)

            influence_total += influence
        
        print('k:         ' + str(i))
        print('max set:   ' + str(max_set))
        print('influence avg: ' + str(float(influence_total)/10) + '\n')

    end = time.time()
    print('time:      ' + str(end - start))

