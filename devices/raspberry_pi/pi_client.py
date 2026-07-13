import requests
from config.settings import settings

class PiClient:

    def __init__(self, host=settings.raspberry_pi["host"], port=settings.raspberry_pi["port"]):

        self.base_url = f"http://{host}:{port}"

    def health(self):

        response = requests.get(
            f"{self.base_url}/",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    def get_tests(self):

        response = requests.get(
            f"{self.base_url}/tests",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    def get_test(self, test_id):

        response = requests.get(
            f"{self.base_url}/tests/{test_id}",
            timeout=5
        )

        response.raise_for_status()

        return response.json()

    def run_test(self, test_id):

        response = requests.post(
            f"{self.base_url}/tests/{test_id}/run",
            timeout=30
        )

        response.raise_for_status()

        return response.json()