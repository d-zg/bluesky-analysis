from graph_utils import load_graph_from_graphml
from client import get_client, get_all_posts
from evading_rate_limits import MultiClient
from sentiment import vader_sentiment
from clearsky import ClearSkyAPI

client = MultiClient()
client.load_env_clients("./.env")

clearsky_api = ClearSkyAPI()

file_path = "./graph_datasets/election_10000_graph.graphml"
graph = load_graph_from_graphml(file_path)

def get_average_sentiment(multi_client, handle):
    posts = get_all_posts(multi_client, "*", 100, "latest", author=handle)
    cumulative = 0
    for post in posts:
        cumulative += vader_sentiment(post.record.text)
    return cumulative / len(posts)

def get_num_blocks(api, handle):
    return api.get_total_blocked_by(handle)


for node_handle in graph.nodes:
    sentiment = get_average_sentiment(client, node_handle)
    blocks = get_num_blocks(clearsky_api, node_handle)
    graph.nodes[node_handle]["sentiment"] = sentiment
    graph.nodes[node_handle]["blocked_by"] = blocks