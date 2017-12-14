import sys
import time

from load import load_snap_graph
from influence import deactivate_all_nodes, node_influence, set_influence


def max_influence_node(network, whitelist=None):
    if whitelist is None:
        whitelist = []

    max_node = None
    max_active = []
    max_influence = 0

    # Check the nodes that haven't been activated
    for node in network.Nodes():
        if node.GetId() not in whitelist:
            deactivate_all_nodes(network, whitelist)

            # Test the influence of this singular node
            influence, active = node_influence(network, node)

            # Update the node with the best influence
            if influence > max_influence:
                max_node = node.GetId()
                max_active = active
                max_influence = influence

    return max_node, max_active, max_influence


def max_influence_set(network, k):
    max_set = []
    whitelist = []
    influence = 0

    for i in range(k):
        # Find the next best node that hasn't already been activated
        # (whitelist are activated nodes)
        max_node, max_active, max_influence = max_influence_node(network, whitelist)
        max_set.append(max_node)
        whitelist.extend(max_active)
        influence += max_influence

        # Print the total influence thus far
        print('k:         ' + str(i + 1))
        print('max set:   ' + str(max_set))
        print('influence: ' + str(influence) + '\n')

    return max_set


if __name__ == '__main__':
    # Parameters
    k = int(sys.argv[1])

    # Load the data
    network = load_snap_graph('../data/wiki-Vote.txt')

    # Find the max influence set of size k
    start = time.time()
    max_set = max_influence_set(network, k)

    # Measure the influence of the set
    influence = set_influence(network, max_set)

    end = time.time()
    print('time:      ' + str(end - start))
