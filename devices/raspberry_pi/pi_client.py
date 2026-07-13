import requests
from config.settings import settings
from models.action import Action
from models.parameter import Parameter

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

    def get_actions(self) -> list[Action]:

        actions = []

        try:
            tests = self.get_tests()

        except requests.RequestException:
            print("⚠ Raspberry Pi offline")
            return actions

        for test in tests:
            actions.append(
                Action(
                    id=f"pi.{test['id']}",
                    name=test["name"],
                    device="raspberry_pi",
                    category="Raspberry Pi",
                    description=test.get("description", ""),
                    parameters=[]
                )
            )

        return actions

    def run_test(self, test_id):

        response = requests.post(
            f"{self.base_url}/tests/{test_id}/run",
            timeout=30
        )

        response.raise_for_status()

        return response.json()