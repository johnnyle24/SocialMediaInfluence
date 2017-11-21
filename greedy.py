import snap

import time
import numpy as np


def deactivate_all_nodes(N):
    for n in N.Nodes():
        N.AddIntAttrDatN(n, 0, 'active')


def node_influence(n, N):
    N.AddIntAttrDatN(n, 1, 'active')
    influence = 1
    stack = [n.GetId()]

    while stack:
        v = N.GetNI(stack.pop())
        for out_edge in v.GetOutEdges():
            w = N.GetNI(N.GetEI(out_edge).GetDstNId())

            # See if inactive neighbor becomes active
            if N.GetIntAttrDatN(w, 'active') == 0:
                threshold = N.GetFltAttrDatN(w, 'threshold')

                # Generate some edge weights (to potentially use later)
                edge_weights = np.random.dirichlet(np.ones(w.GetInDeg())) \
                               * np.random.uniform(0, 1)
                edge_weights = edge_weights.tolist()

                # Compute the activation
                activation = 0
                for in_edge in w.GetInEdges():
                    u = N.GetEI(in_edge).GetSrcNId()
                    active = N.GetIntAttrDatN(u, 'active')
                    weight = N.GetFltAttrDatE(in_edge, 'weight')

                    if weight == -1:
                        weight = edge_weights.pop()
                        N.AddFltAttrDatE(in_edge, weight, 'weight')

                    activation += active * weight

                # Determine if this node becomes active
                if activation > threshold:
                    N.AddIntAttrDatN(w, 1, 'active')
                    influence += 1
                    stack.append(w.GetId())

    return influence


def set_influence(S, N):
    deactivate_all_nodes(N)

    influence = 0
    for n in S:
        n = N.GetNI(n)

        # Only measure influence if not already active
        # (if already active, influence would have already been taken into account)
        if N.GetIntAttrDatN(n, 'active') == 0:
            influence += node_influence(n, N)
    return influence


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
    k = 1

    # Load the network
    N = snap.LoadEdgeList(snap.PNEANet, "wiki-Vote.txt", 0, 1)

    # Initialize attributes
    N.AddIntAttrN('active')
    N.AddFltAttrN('threshold')
    N.AddFltAttrE('weight')

    for n in N.Nodes():
        N.AddIntAttrDatN(n, 0, 'active')
        threshold = np.random.uniform(0, 1)
        N.AddFltAttrDatN(n, threshold, 'threshold')

    for e in N.Edges():
        N.AddFltAttrDatE(e, -1, 'weight')

    # Find the max influence set of size k
    start = time.time()
    S = max_influence_set(k, N)
    end = time.time()
    print('Time to find set: ' + str(end - start))

    # Measure the influence of the set
    influence = set_influence(S, N)
    print('Influence:        ' + str(influence))
