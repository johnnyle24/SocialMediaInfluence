from networkit.graphio import SNAPGraphReader, METISGraphWriter

# Read snap format
reader = SNAPGraphReader()
graph = reader.read('wiki-Vote.txt')

# Write to metis format
writer = METISGraphWriter()
writer.write(graph, 'wiki-Vote-metis.txt')
