import requests
import time
from typing import List, Tuple


class ClearSkyAPI:
    BASE_URL = "https://api.clearsky.services"
    RATE_LIMIT_DELAY = 0.3  # 300ms delay between requests

    def __init__(self):
        self.session = requests.Session()
        self.last_call_time = []

    def close(self):
        """Close the requests session."""
        self.session.close()

    def _rate_limited(self):
        """Ensure a fixed delay between API calls."""
        current_time = time.time()
        if self.last_call_time:
            elapsed_time = current_time - self.last_call_time[-1]
            if elapsed_time < self.RATE_LIMIT_DELAY:
                time.sleep(self.RATE_LIMIT_DELAY - elapsed_time)
        self.last_call_time.append(time.time())
        # Retain only the last timestamp
        if len(self.last_call_time) > 1:
            self.last_call_time = [self.last_call_time[-1]]

    def rate_limited_query(self, endpoint: str):
        """Perform a rate-limited API query."""
        self._rate_limited()
        response = self.session.get(endpoint)
        response.raise_for_status()
        return response.json()

    def get_user_blocklists(self, handle: str) -> List[Tuple[str, str]]:
        """
        Query the /subscribe-blocks-single-blocklist endpoint for a user's blocklists.

        Args:
            handle (str): The handle of the user to query.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing (handle, list_uri).
        """
        endpoint = f"{self.BASE_URL}/api/v1/anon/subscribe-blocks-single-blocklist/{handle}/1"
        data = self.rate_limited_query(endpoint)

        # Extract the blocklist data
        blocklist = data.get("data", {}).get("blocklist", [])
        return [(item["handle"], item["list_uri"]) for item in blocklist]

    def get_total_blocked_by(self, handle: str) -> int:
        """
        Query the total number of users who have blocked a given handle.

        Args:
            handle (str): The handle of the user to query.

        Returns:
            int: The total number of users who have blocked the handle.
        """
        endpoint = f"{self.BASE_URL}/api/v1/anon/single-blocklist/total/{handle}"
        resp = self.rate_limited_query(endpoint)
        if not resp or not resp.get("data", None):
            return -1 # denotes that we couldn't get information for this post
        return resp.get("data", {}).get("count", -1)

    def get_total_blocking(self, handle: str) -> int:
        endpoint = f"{self.BASE_URL}/api/v1/anon/blocklist/total/{handle}"
        resp = self.rate_limited_query(endpoint)
        if not resp or not resp.get("data", None):
            return -1 # denotes that we couldn't get information for this post
        return resp.get("data", {}).get("count", -1)


def main():
    api = ClearSkyAPI()
    try:
        handle = "trumpluvsobama.bsky.social"
        for i in range(5):
            blocklists = api.get_total_blocked_by(handle)
            print(blocklists)
            print("finished")
    finally:
        api.close()


if __name__ == "__main__":
    main()
