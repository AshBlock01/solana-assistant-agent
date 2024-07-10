import unittest
from src.utils import get_price_for_token, get_rug_score

class TestUtils(unittest.TestCase):
    def test_get_price_for_token(self):
        token_name = "bitcoin"
        result = get_price_for_token(token_name)
        self.assertTrue(result.startswith("$") and "." in result)

    def test_get_rug_score(self):
        token_id = "MAXt5moBxMd665GKPx6bammFf5t9pPSG6q7z9Adtm9Z"
        result = get_rug_score(token_id)
        self.assertIn("score", result)

if __name__ == "__main__":
    unittest.main()
