from client import get_client, fetch_thread_data, fetch_reposted_by, fetch_quotes
from graph import build_graph_from_thread
from graph_utils import * # convert_to_networkx, visualize_graph

def main():
    # User credentials and URI
    username = "warrenglover.bsky.social"
    password = "Hearthstone123"
    uri = "at://did:plc:jrhiazkqht2txt7xiixad5v7/app.bsky.feed.post/3lbqfxx3kc22j"

    # Initialize client
    client = get_client(username, password)

    # Fetch thread data
    thread_data = fetch_thread_data(client, uri)
    fetch_quotes(client, uri)
    fetch_reposted_by(client, uri)


    # Build the graph
    root_node, target_node = build_graph_from_thread(thread_data, uri)

    # Convert to NetworkX and visualize
    graph = convert_to_networkx(root_node)
    # visualize_graph(graph)
    centrality_data = record_centrality_measures(graph)
    sorted_nodes = sort_nodes_by_centrality(centrality_data, 'degree_centrality')
    report_top_nodes(sorted_nodes, 'betweenness_centrality', 10)
    echo_chamber_metrics = analyze_echo_chamber_properties(graph)
    print(echo_chamber_metrics)


if __name__ == "__main__":
    main()