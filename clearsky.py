import asyncio
import aiohttp
from typing import List, Tuple


class ClearSkyAPI:
    BASE_URL = "https://api.clearsky.services"
    RATE_LIMIT = 5  # Maximum queries per second

    def __init__(self):
        self.session = aiohttp.ClientSession()
        self.last_call_time = asyncio.Queue(maxsize=self.RATE_LIMIT)
        self.lock = asyncio.Lock()

    async def close(self):
        """Close the aiohttp session."""
        await self.session.close()

    async def _rate_limited(self):
        """Ensure API calls respect the rate limit of 5 calls per second."""
        async with self.lock:
            current_time = asyncio.get_event_loop().time()
            if self.last_call_time.full():
                # Wait for the oldest timestamp to ensure a 1-second interval
                oldest_time = await self.last_call_time.get()
                sleep_duration = max(0, 1 - (current_time - oldest_time))
                if sleep_duration > 0:
                    await asyncio.sleep(sleep_duration)
            # Add the current timestamp
            await self.last_call_time.put(current_time)

    async def rate_limited_query(self, endpoint: str):
        """Perform a rate-limited API query."""
        await self._rate_limited()
        async with self.session.get(endpoint) as response:
            response.raise_for_status()
            return await response.json()

    async def get_user_blocklists(self, handle: str) -> List[Tuple[str, str]]:
        """
        Query the /subscribe-blocks-single-blocklist endpoint for a user's blocklists.

        Args:
            handle (str): The handle of the user to query.

        Returns:
            List[Tuple[str, str]]: A list of tuples containing (handle, list_uri).
        """
        endpoint = f"{self.BASE_URL}/api/v1/anon/subscribe-blocks-single-blocklist/{handle}/1"
        data = await self.rate_limited_query(endpoint)

        # Extract the blocklist data
        blocklist = data.get("data", {}).get("blocklist", [])
        return [(item["handle"], item["list_uri"]) for item in blocklist]


async def main():
    api = ClearSkyAPI()
    try:
        handle = "trumpluvsobama.bsky.social"
        blocklists = await api.get_user_blocklists(handle)
        print(blocklists)
    finally:
        await api.close()


if __name__ == "__main__":
    asyncio.run(main())
