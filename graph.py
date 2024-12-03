from node import Node
from sentiment import vader_sentiment


def build_graph_from_thread(thread_data, uri):
    """Build a graph from thread data."""
    uri_to_node = {}

    def create_node(post):
        return Node(
            text=post.record.text,
            handle=post.author.handle,
            uri=post.uri,
            labels=post.labels,
            like_count=post.like_count,
            quote_count=post.quote_count,
            sentiment=vader_sentiment(post.record.text),
        )

    def parse_thread_view_post(thread_view_post):
        if "$type" in thread_view_post and thread_view_post["$type"] in ["NotFoundPost", "BlockedPost"]:
            return None
        post = thread_view_post.post
        if not post:
            return None
        if post.labels:
            print('here')
        uri = post.uri
        if uri in uri_to_node:
            node = uri_to_node[uri]
        else:
            node = create_node(post)
            uri_to_node[uri] = node

        parent = thread_view_post.parent
        if parent:
            parent_node = parse_thread_view_post(parent)
            if parent_node:
                parent_node.add_reply(node)

        replies = thread_view_post.replies
        for reply in (replies if replies else []):
            reply_node = parse_thread_view_post(reply)
            if reply_node:
                node.add_reply(reply_node)

        return node

    root = parse_thread_view_post(thread_data)
    return root, uri_to_node.get(uri)
