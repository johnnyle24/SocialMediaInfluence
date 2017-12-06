import numpy as np


def deactivate_all_nodes(network, whitelist=None):
    if whitelist is None:
        whitelist = []

    # Whitelist are nodes which should remain active
    for node in network.Nodes():
        if node.GetId() in whitelist:
            network.AddIntAttrDatN(node, 1, 'active')
        else:
            network.AddIntAttrDatN(node, 0, 'active')


def node_influence(network, node):
    network.AddIntAttrDatN(node, 1, 'active')
    stack = [node.GetId()]

    influence = 1
    active = [node.GetId()]
    while stack:
        u = network.GetNI(stack.pop())
        for out_edge in range(u.GetOutDeg()):
            v = network.GetNI(u.GetOutNId(out_edge))

            # See if inactive neighbor becomes active
            if network.GetIntAttrDatN(v, 'active') == 0:
                threshold = network.GetFltAttrDatN(v, 'threshold')

                # Generate some edge weights (to potentially use later)
                edge_weights = np.random.dirichlet(np.ones(v.GetInDeg())) * np.random.uniform(0, 1)
                edge_weights = edge_weights.tolist()

                # Compute the activation
                activation = 0
                for in_edge in range(v.GetInDeg()):
                    w = v.GetInNId(in_edge)
                    edge = network.GetEI(w, v.GetId())
                    is_active = network.GetIntAttrDatN(w, 'active')
                    weight = network.GetFltAttrDatE(edge, 'weight')

                    if weight == -1:
                        weight = edge_weights.pop()
                        network.AddFltAttrDatE(edge, weight, 'weight')

                    activation += is_active * weight

                # Determine if this node becomes active
                if activation > threshold:
                    network.AddIntAttrDatN(v, 1, 'active')
                    stack.append(v.GetId())

                    influence += 1
                    active.append(v.GetId())

    return influence, active


def set_influence(network, max_set):
    deactivate_all_nodes(network)

    influence = 0
    for node in max_set:
        node = network.GetNI(node)

        # Only measure influence if not already active
        # (if already active, influence would have already been taken into account)
        if network.GetIntAttrDatN(node, 'active') == 0:
            influence += node_influence(network, node)[0]
    return influence
