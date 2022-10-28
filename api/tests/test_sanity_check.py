import requests
import unittest

# Test deployment at art-build-dev Openshift namespace
API = "http://localhost:8080"


class TestSanityCheck(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        endpoint = f"{API}/test"
        cls.response = requests.get(endpoint)

    def test_1(self):
        assert self.response.status_code == 200
