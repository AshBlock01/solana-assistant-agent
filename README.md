# Solana Assistant Agent

This repository contains a Python-based smart assistant for cryptocurrency information using LangChain and Groq. The assistant can fetch real-time token prices and rug scores for Solana memecoin tokens.

## Features

- **Fetch Token Prices:** Retrieve the latest price for a given token from the Pyth Network and convert it to a human-readable format.
- **Check Rug Scores:** Get the rug score for a specific Solana memecoin token ID from the Rug Check API.
- **Interactive Agent:** A smart agent that utilizes LangChain and Groq to interactively answer queries about cryptocurrencies.

## Installation

To use this code, you need to have Python installed. You can install the required dependencies using pip:

```bash```
pip install -r requirements.txt

## Usage
Smart Assistant
The smart assistant uses LangChain and Groq to process user queries and provide relevant information.

To use the agent, update the API_KEY, messages, and thread with your desired content and token information in agent.py.

# Sample Input and Output
Example 1: Checking Rug Score

```python
messages = [HumanMessage(content="is this rug MAXt5moBxMd665GKPx6bammFf5t9pPSG6q7z9Adtm9Z")]
thread = {"configurable": {"thread_id": "2"}}

result = agent.graph.invoke({"messages": messages}, thread)
print(result['messages'][-1].content)
```

Expected Output:
```
The rug score for MAXt5moBxMd665GKPx6bammFf5t9pPSG6q7z9Adtm9Z is 400.
The risks flagged are "Low amount of LP Providers" with a score of 300 and "Mutable metadata" with a score of 100.
```

Example 2: Fetching Bitcoin Price
```python
messages = [HumanMessage(content="what is BTC price")]
thread = {"configurable": {"thread_id": "2"}}

result = agent.graph.invoke({"messages": messages}, thread)
print(result['messages'][-1].content)
```
Expected Output:
```The price of BTC is $57945.65.
```

Replace the following placeholders with your actual information:

API_KEY: Your Groq API key.
messages: The content of the message you want to send to the assistant.
thread: The configuration for the thread you want to use.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request if you have any suggestions or improvements.

