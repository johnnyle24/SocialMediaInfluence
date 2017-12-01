from nxmetis import partition
from metisreader import MetisReader

# Read the graph
reader = MetisReader('wiki-Vote-metis.txt')
reader.read()
graph = reader.get_graph()

# Partition the graph
part = partition(graph, 2)[1]
left = graph.subgraph(part[0])
right = graph.subgraph(part[1])

# Save the graph
