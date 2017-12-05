import numpy as np

from networkx import Graph
from snap import LoadEdgeList, PNEANet


def load_snap_graph(path):
    # Load the network
    graph = LoadEdgeList(PNEANet, path, 0, 1)

    # Initialize attributes
    graph.AddIntAttrN('active')
    graph.AddFltAttrN('threshold')
    graph.AddFltAttrE('weight')

    for n in graph.Nodes():
        graph.AddIntAttrDatN(n, 0, 'active')
        threshold = np.random.uniform(0, 1)
        graph.AddFltAttrDatN(n, threshold, 'threshold')

    for e in graph.Edges():
        graph.AddFltAttrDatE(e, -1, 'weight')

    return graph


def load_networkx_graph(path):
    # Inefficient, could be refactored
    graph = Graph()
    with open(path) as f:
        for line in f:
            if not line.startswith('#'):
                first, second = line.split()
                first = int(first)
                second = int(second)

                graph.add_node(first)
                graph.add_node(second)
                graph.add_edge(first, second)

    return graph
