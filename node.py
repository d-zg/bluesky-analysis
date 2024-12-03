class Node:
    def __init__(self, text, handle, uri, labels, like_count, quote_count, sentiment):
        self.text = text
        self.handle = handle
        self.uri = uri
        self.labels = labels
        self.like_count = like_count
        self.quote_count = quote_count
        self.parent = None
        self.replies = []
        self.sentiment = sentiment

    def add_reply(self, reply_node):
        self.replies.append(reply_node)
        reply_node.parent = self
