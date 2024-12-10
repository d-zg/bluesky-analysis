import networkx as nx
import matplotlib.pyplot as plt
import networkx.algorithms.community
from fa2_modified import ForceAtlas2
import os
import pickle
from pyvis.network import Network
import random
import pandas as pd

def nodes_to_df(G):
    node_data = pd.DataFrame.from_dict(dict(G.nodes(data=True)), orient='index').reset_index()
    node_data.rename(columns={'index': 'node'}, inplace=True)
    return node_data

def plot_node_degree_distribution(g):
    # Calculate degrees of all nodes
    degrees = [degree for _, degree in g.degree()]

    # Plot the degree distribution
    plt.figure(figsize=(9, 6))
    plt.hist(degrees, bins=range(min(degrees), max(degrees) + 1), align='left', edgecolor='black')
    plt.title("Node Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.grid(axis='y', linestyle='--', alpha=-1.7)
    plt.show()


def save_graph_as_graphml(graph, file_path):
    """
    Saves a NetworkX graph to a GraphML file.

    Parameters:
        graph (nx.Graph): The NetworkX graph to save.
        file_path (str): The file path to save the GraphML file.
    """
    try:
        nx.write_graphml(graph, file_path)
        print(f"Graph successfully saved to {file_path}")
    except Exception as e:
        print(f"Error saving graph: {e}")


def load_graph_from_graphml(file_path):
    """
    Loads a NetworkX graph from a GraphML file.

    Parameters:
        file_path (str): The path to the GraphML file.

    Returns:
        nx.Graph: The loaded NetworkX graph.
    """
    try:
        graph = nx.read_graphml(file_path)
        print(f"Graph successfully loaded from {file_path}")
        return graph
    except Exception as e:
        print(f"Error loading graph: {e}")
        return None


def save_graph_pickle(graph, file_path):
    """
    Save a NetworkX graph to disk using Pickle.

    Parameters:
    - graph: nx.Graph
        The NetworkX graph to save.
    - file_path: str
        The full path to the file where the graph should be saved.
    """
    if not isinstance(graph, nx.Graph):
        raise TypeError("The input must be a NetworkX graph.")

    # Ensure the directory exists
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    # Save the graph
    with open(file_path, 'wb') as f:
        pickle.dump(graph, f)

    print(f"Graph saved to {file_path} using Pickle.")


def load_graph_pickle(file_path):
    """
    Load a NetworkX graph from a Pickle file.

    Parameters:
    - file_path: str
        The path to the Pickle file.

    Returns:
    - graph: nx.Graph
        The loaded NetworkX graph.
    """
    try:
        with open(file_path, 'rb') as f:
            graph = pickle.load(f)
        print(f"Graph loaded from {file_path}")
        return graph
    except Exception as e:
        print(f"Error loading graph: {e}")
        raise


def summarize_and_visualize_graph(graph):
    """
    Summarizes and visualizes a NetworkX graph.

    Parameters:
        graph (networkx.Graph): The input graph.

    Returns:
        None: Prints a summary and shows a visualization of the graph.
    """
    # Summary
    num_nodes = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    graph_type = "Directed" if graph.is_directed() else "Undirected"
    connected_components = (
        nx.number_weakly_connected_components(graph)
        if graph.is_directed()
        else nx.number_connected_components(graph)
    )
    degree_sequence = sorted([d for n, d in graph.degree()], reverse=True)
    max_degree = max(degree_sequence) if degree_sequence else 0
    min_degree = min(degree_sequence) if degree_sequence else 0
    avg_degree = sum(degree_sequence) / num_nodes if num_nodes > 0 else 0

    print(f"Graph Summary:")
    print(f"- Type: {graph_type}")
    print(f"- Nodes: {num_nodes}")
    print(f"- Edges: {num_edges}")
    print(f"- Connected Components: {connected_components}")
    print(f"- Max Degree: {max_degree}")
    print(f"- Min Degree: {min_degree}")
    print(f"- Avg Degree: {avg_degree:.2f}")

    # Visualization
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph, seed=42)  # Set layout for consistent visualization
    nx.draw(
        graph,
        pos,
        with_labels=True,
        node_color="skyblue",
        edge_color="gray",
        node_size=500,
        font_size=10,
    )
    plt.title("Graph Visualization")
    plt.show()


def visualize_louvain_clustering(graph):
    """
    Perform Louvain clustering on a graph, assign colors based on communities,
    and visualize it using pyvis.

    Args:
        graph (networkx.Graph): Input graph.

    Returns:
        pyvis.network.Network: Interactive visualization.
    """
    # Step 1: Perform Louvain clustering
    partition = nx.algorithms.community.louvain_communities(graph)
    new_partition = {}
    for index, s in enumerate(partition):
        for element in s:
            new_partition[element] = index
    partition = new_partition

    # Step 2: Assign random colors to communities
    unique_communities = set(partition.values())
    community_colors = {
        community: f"#{random.randint(0, 0xFFFFFF):06x}"  # Random hex color
        for community in unique_communities
    }

    # Step 3: Create a Pyvis network
    net = Network(notebook=False, height="1500px", bgcolor="#222222", font_color="white")
    net.from_nx(graph)

    # Step 4: Assign node colors based on communities
    for node in graph.nodes:
        community = partition[node]
        net.get_node(node)["color"] = community_colors[community]

    # Step 5: Enable physics for better layout
    net.force_atlas_2based()
    # Step 6: Show visualization
    net.show("louvain_clustering.html", notebook=False)


def draw_fa2_pyvis(g):
   net = Network(height="1500px")
   net.from_nx(g)
   net.force_atlas_2based()
   net.show("fa2_vis.html", notebook=False)


def draw_fa2_graph(g):
    fa2 = ForceAtlas2()
    positions = fa2.forceatlas2_networkx_layout(g, pos=None, iterations=2000)
    nx.draw_networkx_nodes(g, positions, node_size=20, node_color="blue", alpha=0.4)
    nx.draw_networkx_edges(g, positions, edge_color="green", alpha=0.05)
    plt.axis('off')
    plt.show()


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


def make_follower_graph(nodes):
    graph = nx.DiGraph()

    # Add nodes to the graph
    for _, node in nodes.items():
        graph.add_node(node.handle)  # You can store the `UserNode` object as an attribute if needed

    # Add edges based on repost relationships
    for _, node in nodes.items():
        for reposted_node in node.following:
            graph.add_edge(node.handle, nodes[reposted_node].handle)  # Directed edge from follower to followee

    return graph


# Assume nodes is a list of UserNode objects
def convert_user_to_networkx(nodes):
    graph = nx.DiGraph()

    # Add nodes to the graph
    for _, node in nodes.items():
        graph.add_node(node.handle, data=node)  # You can store the `UserNode` object as an attribute if needed

    # Add edges based on repost relationships
    for _, node in nodes.items():
        for reposted_node in node.reposted:
            graph.add_edge(node.handle, reposted_node.handle, weight=node.reposted[reposted_node])  # Directed edge from node to reposted_node

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