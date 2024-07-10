import requests
from langchain_core.tools import tool

def get_price_id(token_name):
    url = f"https://hermes.pyth.network/v2/price_feeds?query={token_name}&asset_type=crypto"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error: Unable to fetch data, received status code {response.status_code}"
    data = response.json()
    if not data:
        return "Error: No data found for the given token name"
    price_id = data[0]['id']
    return price_id

def get_human_readable_price(price_id):
    url = f"https://hermes.pyth.network/v2/updates/price/latest?ids%5B%5D={price_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error: Unable to fetch data, received status code {response.status_code}"
    data = response.json()
    if 'parsed' not in data or len(data['parsed']) == 0:
        return "Error: 'parsed' key not found or is empty in the response"
    price_str = data['parsed'][0]['price']['price']
    expo = data['parsed'][0]['price']['expo']
    price = int(price_str) * (10 ** expo)
    price = f"${price:.2f}"
    return price

@tool
def get_price_for_token(token_name: str) -> str:
    """Fetches the latest price for a given token name from the Pyth Network and converts it to a human-readable format."""
    price_id = get_price_id(token_name)
    if "Error" in price_id:
        return price_id
    return get_human_readable_price(price_id)

def check_rug_score(token_id):
    url = f"https://api.rugcheck.xyz/v1/tokens/{token_id}/report/summary"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Error: Unable to fetch data, received status code {response.status_code}"
    data = response.json()
    return data

@tool
def get_rug_score(token_id: str) -> str:
    """Fetches the rug score for a given Solana memecoin token ID from the Rug Check API."""
    score = check_rug_score(token_id)
    return score
