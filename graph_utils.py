import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community


def convert_to_networkx(root_node):
    """Convert the custom graph to a NetworkX graph."""
    graph = nx.DiGraph()

    def add_nodes_and_edges(node):
        graph.add_node(
            node.uri,
            text=node.text,
            handle=node.handle,
            labels=node.labels,
            like_count=node.like_count,
            quote_count=node.quote_count,
            sentiment=node.sentiment,
        )
        for reply in (node.replies if node.replies else []):
            graph.add_edge(node.uri, reply.uri)
            add_nodes_and_edges(reply)

    add_nodes_and_edges(root_node)
    return graph

def visualize_graph(graph):
    """Visualize a NetworkX graph."""
    plt.figure(figsize=(10, 10))
    pos = nx.spring_layout(graph)

    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(graph, pos, arrows=True)

    labels = {node: graph.nodes[node].get("text", node)[:10] for node in graph.nodes}
    nx.draw_networkx_labels(graph, pos, labels, font_size=10, font_color="black")

    plt.title("Graph Visualization", fontsize=15)
    plt.axis("off")
    plt.show()


import networkx as nx

def record_centrality_measures(graph):
    """
    Records degree and betweenness centrality for all nodes in the graph.

    Parameters:
        graph (networkx.Graph or networkx.DiGraph): The input graph.

    Returns:
        dict: A dictionary where each key is a node, and the value is another dictionary with:
              - 'degree_centrality'
              - 'betweenness_centrality'
    """
    # Compute centrality metrics
    degree_centrality = nx.degree_centrality(graph)
    betweenness_centrality = nx.betweenness_centrality(graph)

    # Record metrics for each node
    centrality_data = {}
    for node in graph.nodes:
        node_data = graph.nodes[node]  # Get node attributes
        centrality_data[node] = {
            'degree_centrality': degree_centrality.get(node, 0),
            'betweenness_centrality': betweenness_centrality.get(node, 0),
            'text': node_data.get('text', 'N/A'),
            'labels': node_data.get('labels', []),
            'sentiment': node_data.get('sentiment', 'N')
        }

    return centrality_data

def sort_nodes_by_centrality(centrality_data, metric):
    """
    Sorts nodes by a specified centrality metric.

    Parameters:
        centrality_data (dict): The centrality data dictionary returned by record_centrality_measures.
        metric (str): The centrality metric to sort by (e.g., 'degree_centrality', 'betweenness_centrality').

    Returns:
        list: A list of tuples, where each tuple contains a node and its centrality value, sorted in descending order of the metric.
    """
    if metric not in ['degree_centrality', 'betweenness_centrality']:
        raise ValueError(f"Invalid metric: {metric}. Choose 'degree_centrality' or 'betweenness_centrality'.")

    # Sort nodes by the specified metric
    sorted_nodes = sorted(
        centrality_data.items(),
        key=lambda item: item[1][metric],
        reverse=True
    )
    return sorted_nodes

def report_top_nodes(sorted_nodes, metric, top_x):
    """
    Reports the top X nodes based on a specified centrality metric, including their text and labels.

    Parameters:
        sorted_nodes (list): A sorted list of tuples returned by sort_nodes_by_centrality.
        metric (str): The centrality metric used for sorting.
        top_x (int): The number of top nodes to report.

    Returns:
        None
    """
    print(f"Top {top_x} nodes by {metric}:")
    print("========================")
    for i, (node, centrality_values) in enumerate(sorted_nodes[:top_x], 1):
        text = centrality_values.get('text', 'N/A')
        labels = ', '.join(centrality_values.get('labels', []))
        sentiment = centrality_values.get('sentiment', 0)
        print(f"{i}. Node: {node}, {metric}: {centrality_values[metric]:.4f}")
        print(f"   Text: {text}")
        print(f"   Labels: {labels}")
        print(f"   Sentiment: {sentiment}")



def analyze_echo_chamber_properties(graph):
    """
    Analyze metrics commonly used to measure the echo chamber properties of a graph.

    Parameters:
        graph (networkx.Graph or networkx.DiGraph): The input graph.

    Returns:
        dict: A dictionary containing key echo chamber metrics.
    """
    # Modularity
    communities = list(networkx.algorithms.community.greedy_modularity_communities(graph.to_undirected()))
    modularity = nx.algorithms.community.quality.modularity(graph.to_undirected(), communities)

    # Assortativity (e.g., by an 'opinion' attribute if present)
    if 'opinion' in next(iter(graph.nodes(data=True)))[1]:
        assortativity = nx.attribute_assortativity_coefficient(graph, 'opinion')
    else:
        assortativity = None

    # Edge homogeneity (manual calculation based on attributes)
    edge_homogeneity = sum(
        1 for u, v in graph.edges
        if graph.nodes[u].get('opinion') == graph.nodes[v].get('opinion')
    ) / graph.number_of_edges() if graph.number_of_edges() > 0 else 0

    # Density of the graph
    density = nx.density(graph)

    return {
        'modularity': modularity,
        'assortativity': assortativity,
        'edge_homogeneity': edge_homogeneity,
        'density': density,
    }