from client import get_client, get_all_posts, fetch_followers, get_all_following, get_all_followers
from node import UserNode
from graph_utils import make_follower_graph, visualize_graph, draw_fa2_graph, save_graph_as_graphml
from evading_rate_limits import MultiClient

from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import time

lock = threading.Lock()
client = MultiClient()
client.load_env_clients("./.env")


def process_user(handle, nodes, multi_client, finished, max_edges):
    with lock:
        if handle in finished:
            return
        finished.add(handle)
    followers = get_all_following(multi_client, handle, max_edges)

    for follower in followers:
        with lock:
            if follower.handle in nodes:
                nodes[handle].add_follower(nodes[follower.handle])


def build_subgraph(client, query, num_nodes):
    nodes = {}
    posts = get_all_posts(client, query, num_nodes)
    for post in posts:
        nodes[post.author.handle] = UserNode(post.author.handle)

    finished = set()
    max_edges = 1000
    delay = 2
    with ThreadPoolExecutor() as executor:
        futures = []
        for post in posts:
            futures.append(executor.submit(process_user, post.author.handle, nodes, client, finished, max_edges))
            time.sleep(delay)
        # futures = [executor.submit(process_user, post.author.handle, nodes, client, finished, max_edges) for post in posts]
        for future in as_completed(futures):
            try:
                future.result()  # Ensure exceptions in threads are raised
            except Exception as e:
                print(f"Error processing a post: {e}")
    return nodes

query = "election"
num_nodes = 100000
subgraph = build_subgraph(client, query, num_nodes)
G = make_follower_graph(subgraph)
save_graph_as_graphml(G, f"./graph_datasets/{query}_{num_nodes}_graph")
draw_fa2_graph(G)


