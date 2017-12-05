import time

from load import load_snap_graph
from influence import deactivate_all_nodes, node_influence, set_influence


def max_influence_node(S, N):
    max_n = None
    max_influence = 0

    for n in N.Nodes():
        if n.GetId() not in S:
            deactivate_all_nodes(N)

            # Test the influence of this singular node
            influence = node_influence(n, N)

            # Update the node with the best influence
            if influence > max_influence:
                max_n = n.GetId()
                max_influence = influence

    return max_n, max_influence


def max_influence_set(k, N):
    S = []
    for i in range(k):
        max_n, max_influence = max_influence_node(S, N)
        S.append(max_n)
    return S


if __name__ == '__main__':
    # Parameters
    k = 4

    # Load the data
    N = load_snap_graph('../data/wiki-Vote.txt')

    # Find the max influence set of size k
    start = time.time()
    S = max_influence_set(k, N)
    end = time.time()
    print('Time to find set: ' + str(end - start))

    # Measure the influence of the set
    influence = set_influence(S, N)
    print('Influence:        ' + str(influence))
