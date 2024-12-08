from graph_utils import load_graph_from_graphml, summarize_and_visualize_graph, draw_fa2_graph

g = load_graph_from_graphml("./graph_datasets/election_10000_graph")
draw_fa2_graph(g)