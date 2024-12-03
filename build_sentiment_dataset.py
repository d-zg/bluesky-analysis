from client import get_client, get_all_posts
from sentiment import vader_sentiment
import argparse
import pandas as pd
from datetime import datetime


def save_posts_to_dataframe(posts):
    """
    Save posts data to a DataFrame with `uri` as the primary key.

    Args:
        posts (list): A list of post objects, each having attributes accessed similarly to create_node.

    Returns:
        pd.DataFrame: A DataFrame containing post data.
    """
    data = []

    for post in posts:
        data.append({
            "uri": post.uri,
            "text": post.record.text,
            "handle": post.author.handle,
            "labels": post.labels,
            "like_count": post.like_count,
            "quote_count": post.quote_count,
            "repost_count": post.repost_count,
            "sentiment": vader_sentiment(post.record.text),
        })

    # Convert to a DataFrame
    df = pd.DataFrame(data)

    # Set `uri` as the primary key (index)
    df.set_index("uri", inplace=True)

    return df


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process some inputs.")
    parser.add_argument("query", type=str, nargs="?", default="vaccines", help="Query string to process.")
    parser.add_argument("filename", type=str, nargs="?", default=None, help="Path to the output file.")
    parser.add_argument("dataset_size", type=int, nargs="?", default=10000, help="Size of the dataset.")
    args = parser.parse_args()

    if args.filename is None:
        current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
        args.filename = f"{args.query}_{args.dataset_size}_{current_datetime}.csv"

    return args

if __name__ == '__main__':
    args = parse_arguments()
    username = "warrenglover.bsky.social"
    password = "Hearthstone123"
    client = get_client(username, password)
    posts = get_all_posts(client, args.query, args.dataset_size)
    df = save_posts_to_dataframe(posts)
    df.to_csv(args.filename)

