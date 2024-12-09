from graph_utils import load_graph_from_graphml, summarize_and_visualize_graph, draw_fa2_graph, draw_fa2_pyvis, visualize_louvain_clustering
import matplotlib.pyplot as plt
import random


G = load_graph_from_graphml("./graph_datasets/election_10000_graph")

filtered_nodes = [node for node, degree in G.degree() if degree > 10]

# Step 2: Create a subgraph with these filtered nodes
filtered_subgraph = G.subgraph(filtered_nodes).copy()

# Step 3: Randomly sample 1000 nodes from the filtered subgraph
sampled_nodes = random.sample(list(filtered_subgraph.nodes()), min(400, len(filtered_subgraph)))

# Step 4: Create a subgraph with the sampled nodes
final_subgraph = G.subgraph(sampled_nodes).copy()
visualize_louvain_clustering(final_subgraph)
# draw_fa2_pyvis(final_subgraph)