from atproto import Client


def get_client(username, password):
    """Authenticate and return a Bluesky API client."""
    client = Client()
    client.login(username, password)
    return client


def fetch_thread_data(client, uri):
    """Fetch thread data for the given URI using the client."""
    res = client.get_post_thread(uri=uri)
    return res.thread


def get_posts(client, query):
    """
    :param client: bluesky client
    :param query: query word
    :return: list of post objects
    """
    params = {"q": query, "limit": 100}
    resp = client.app.bsky.feed.search_posts(params=params)
    posts = resp.posts
    return posts


def get_all_posts(client, query, max_results=None):
    """
    Retrieve all posts, or max_results matching a query using pagination

    Args:
        client: Bluesky client instance.
        query (str): Query word.
        max_results (int, optional): Maximum number of posts to fetch. If None, fetch all available posts.

    Returns:
        pd.DataFrame: A DataFrame containing all retrieved posts.
    """
    params = {"q": query, "limit": 100}
    all_posts = []
    total_fetched = 0

    while True:
        # Fetch posts
        resp = client.app.bsky.feed.search_posts(params=params)
        posts = resp.posts
        all_posts.extend(posts)

        # Update the total fetched count
        total_fetched += len(posts)

        # Check if we should stop fetching
        if max_results and total_fetched >= max_results:
            all_posts = all_posts[:max_results]  # Trim excess posts
            break

        # Check for the next cursor
        cursor = getattr(resp, 'cursor', None)
        if not cursor:
            break

        # Update params with the cursor
        params["cursor"] = cursor

    return all_posts


def fetch_quotes(client, uri):
    params = {"uri": uri}
    resp = client.app.bsky.feed.get_quotes(params=params)
    return resp.posts


def fetch_reposted_by(client, uri):
    params = {"uri": uri}
    resp = client.app.bsky.feed.get_reposted_by(params=params)
    return resp
