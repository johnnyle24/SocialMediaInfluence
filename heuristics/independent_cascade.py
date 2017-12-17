import numpy as np
import pdb as p


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

                edge = network.GetEI(u.GetId(), v.GetId())

                probability = network.GetFltAttrDatE(edge, 'weight')

                if probability == -1:
                    # Calculate edge activation probability
                    # probability = np.random.uniform(0,1)
                    probability = 0.10
                    network.AddFltAttrDatE(edge, probability, 'weight')

                # Check the value of the biased coin
                flipped_value = np.random.uniform(0,1)

                # Check if the value is within the probability bound
                if(flipped_value <= probability):
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
