import logging
from graph_utils import load_graph_from_graphml, save_graph_as_graphml
from client import get_client, get_all_posts
from evading_rate_limits import MultiClient
from sentiment import vader_sentiment
from clearsky import ClearSkyAPI
from add_echo_chamber_metrics import get_model_and_tokenizer, get_classification
from time import sleep
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("script_log.log"),
        logging.StreamHandler()
    ]
)

client = MultiClient()
client.load_env_clients("./.env")

clearsky_api = ClearSkyAPI()

file_path = "./graph_datasets/election_10000_graph"
graph = load_graph_from_graphml(file_path)

def get_average_sentiment_and_leaning(multi_client, handle, model, tokenizer):
    try:
        posts = get_all_posts(multi_client, "*", 100, "latest", author=handle)
        cumulative_sentiment = 0
        cumulative_leaning = 0
        for post in posts:
            cumulative_sentiment += vader_sentiment(post.record.text)
            cumulative_leaning += get_classification(model, tokenizer, post.record.text)
        return cumulative_sentiment / len(posts), cumulative_leaning / len(posts)
    except Exception as e:
        logging.error(f"Error calculating sentiment and leaning for {handle}: {e}")
        return -2, -2

def get_num_blocks(api, handle):
    try:
        return api.get_total_blocked_by(handle)
    except Exception as e:
        logging.error(f"Error processing blocks for {handle}: {e}")
        return -1

def get_num_blocking(api, handle):
    try:
        return api.get_total_blocking(handle)
    except Exception as e:
        logging.error(f"Error processing blocking for {handle}: {e}")
        return -1

i = 0
model, tokenizer = get_model_and_tokenizer()
start_time = time.time()
logging.info("Script started.")

for node_handle in graph.nodes:
    if i % 100 == 0:
        logging.info(f"Processing node {i}: {node_handle}")
    try:
        sentiment, leaning = get_average_sentiment_and_leaning(client, node_handle, model, tokenizer)
        blocks = get_num_blocks(clearsky_api, node_handle)
        blocking = get_num_blocking(clearsky_api, node_handle)
        graph.nodes[node_handle]["sentiment"] = sentiment
        graph.nodes[node_handle]["leaning"] = leaning
        graph.nodes[node_handle]["blocked_by"] = blocks
        graph.nodes[node_handle]["blocking"] = blocking
    except Exception as e:
        logging.error(f"Unexpected error for node {node_handle}: {e}")
    i += 1

end_time = time.time()
duration = end_time - start_time

logging.info(f"Script completed. Duration: {duration} seconds.")
save_graph_as_graphml(graph, "./graph_datasets/election_10000_graph_sentiment_block_leaning_full")
logging.info("Graph saved.")
