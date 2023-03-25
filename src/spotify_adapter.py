import requests


class SpotifyAdapter:

    def __init__(self, token: str):
        self.token = token
        self.header = {"Authorization": f"Bearer {self.token}"}




