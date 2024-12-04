from client import get_all_posts, fetch_reposted_by, get_client
from node import UserNode
from graph_utils import convert_user_to_networkx, draw_fa2_graph
from concurrent.futures import ThreadPoolExecutor, as_completed

import argparse
from datetime import datetime


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

def process_post(post, nodes, client):
    if post.author.handle not in nodes:
        new_node = UserNode(post.author.handle)
        nodes[post.author.handle] = new_node
    response = fetch_reposted_by(client, post.uri)
    for repost_profile in response.reposted_by:
        if repost_profile.handle not in nodes:
            nodes[repost_profile.handle] = UserNode(repost_profile.handle)
        nodes[post.author.handle].add_reposted_by(nodes[repost_profile.handle])

def process_posts_threaded(posts, client):
    nodes = {}
    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_post, post, nodes, client) for post in posts]
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
    draw_fa2_graph(graph)
