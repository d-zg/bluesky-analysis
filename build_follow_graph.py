from client import get_all_posts, fetch_followers, get_client
from node import UserNode
from graph_utils import convert_user_to_networkx, draw_fa2_graph, summarize_and_visualize_graph, save_graph_pickle
from concurrent.futures import ThreadPoolExecutor, as_completed

import argparse
from datetime import datetime
import threading

lock = threading.Lock()

def parse_arguments():
    parser = argparse.ArgumentParser(description="Process some inputs.")
    parser.add_argument("query", type=str, nargs="?", default="ballots", help="Query string to process.")
    parser.add_argument("filename", type=str, nargs="?", default=None, help="Path to the output file.")
    parser.add_argument("dataset_size", type=int, nargs="?", default=1, help="Size of the dataset.")
    args = parser.parse_args()

    if args.filename is None:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.filename = f"{args.query}_{args.dataset_size}_{current_datetime}.csv"

    return args

def process_user(handle, nodes, client, depth):
    if depth == 2: # max depth
        return
    with lock:
        if handle not in nodes:
            new_node = UserNode(handle)
            nodes[handle] = new_node
    response = fetch_followers(client, handle)

    for follower in response.followers:
        search = False
        with lock:
            if follower.handle not in nodes:
                nodes[follower.handle] = UserNode(follower.handle)
                search = True
        if search:
            process_user(follower.handle, nodes, client, depth + 1)
        with lock:
            nodes[handle].add_reposted_by(nodes[follower.handle])

def process_posts_threaded(posts, client):
    nodes = {}
    for post in posts:
        resp = process_user(post.author.handle, nodes, client, 0)
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_user, post.author.handle, nodes, client, 0) for post in posts]
        for future in as_completed(futures):
            try:
                future.result()  # Ensure exceptions in threads are raised
            except Exception as e:
                print(f"Error processing a post: {e}")
    return nodes



if __name__ == '__main__':
    args = parse_arguments()
    username = "warrenglover.bsky.social"
    password = "Hearthstone123"
    client = get_client(username, password)
    posts = get_all_posts(client, args.query, args.dataset_size)
    nodes = process_posts_threaded(posts, client)
    graph = convert_user_to_networkx(nodes)
    save_graph_pickle(graph, "./graph_datasets/testgraph.pkl")

    draw_fa2_graph(graph)
    summarize_and_visualize_graph(graph)
