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
