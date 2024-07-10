import unittest
from src.agent import Agent
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage

class TestAgent(unittest.TestCase):
    def setUp(self):
        API_KEY = "your_api_key_here"
        prompt = "You are an expert smart assistant for crypto. Use the search API engine to look up information and provide your full analysis."
        model = ChatGroq(model_name="gemma2-9b-it", api_key=API_KEY)
        from src.utils import get_price_for_token, get_rug_score
        self.agent = Agent(model, [get_price_for_token, get_rug_score], system=prompt)

    def test_rug_score(self):
        messages = [HumanMessage(content="is this rug MAXt5moBxMd665GKPx6bammFf5t9pPSG6q7z9Adtm9Z")]
        thread = {"configurable": {"thread_id": "2"}}
        result = self.agent.graph.invoke({"messages": messages}, thread)
        self.assertIn("rug score", result['messages'][-1].content)

    def test_btc_price(self):
        messages = [HumanMessage(content="what is BTC price")]
        thread = {"configurable": {"thread_id": "2"}}
        result = self.agent.graph.invoke({"messages": messages}, thread)
        self.assertIn("price of BTC", result['messages'][-1].content)

if __name__ == "__main__":
    unittest.main()
