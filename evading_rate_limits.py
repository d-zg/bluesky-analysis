from client import get_client

import os
from dotenv import load_dotenv
import threading

class MultiClient:
    def __init__(self):
        self.clients = []  # List to store client details
        self.lock = threading.Lock()  # Lock for thread safety
        self.index = 0  # Current index for round-robin selection

    def add_client(self, username, password):
        """
        Add a new client with a username and password.
        """
        new_client = get_client(username, password)
        with self.lock:
            self.clients.append(new_client)

    def get_client(self):
        """
        Retrieve a client in a round-robin manner. Thread-safe.
        """
        with self.lock:
            if not self.clients:
                raise ValueError("No clients available")

            client = self.clients[self.index]
            self.index = (self.index + 1) % len(self.clients)
            return client

    def load_env_clients(self, env_file):
        """
        Load clients from a .env file into the MultiClient instance.

        Args:
            env_file (str): Path to the .env file.
        """
        # Load the .env file
        load_dotenv(env_file)

        # Iterate over environment variables to find CLIENTX_USERNAME and CLIENTX_PASSWORD
        idx = 1
        while True:
            username = os.getenv(f"CLIENT{idx}_USERNAME")
            password = os.getenv(f"CLIENT{idx}_PASSWORD")

            # Stop when there are no more clients
            if not username or not password:
                break

            # Add the client to the MultiClient instance
            self.add_client(username, password)
            idx += 1

