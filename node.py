from collections import defaultdict

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


class UserNode:
    def __init__(self, handle):
        self.handle = handle
        self.reposted = defaultdict(int)
        self.reposted_by = defaultdict(int)
        self.followed_by = {}
        self.following = {}

    def add_repost(self, other):
        self.reposted[other] += 1
        other.reposted_by[self] += 1

    def add_reposted_by(self, other):
        self.reposted_by[other] += 1
        other.reposted[self] += 1

    def add_follower(self, other):
        self.followed_by[other.handle] = other
        other.following[self.handle] = self

    def add_following(self, other):
        other.add_follower(self)