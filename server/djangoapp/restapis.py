import os
import requests
from dotenv import load_dotenv
from urllib.parse import urlencode


load_dotenv()


BACKEND_URL = os.getenv(
    'backend_url',
    default='http://localhost:3030',
)
SENTIMENT_ANALYZER_URL = os.getenv(
    'sentiment_analyzer_url',
    default='http://localhost:5050/',
)


def get_request(endpoint, **kwargs):
    """Send a GET request to the backend."""
    query_string = urlencode(kwargs)
    url = f'{BACKEND_URL}{endpoint}'
    if query_string:
        url = f'{url}?{query_string}'
    print(f'GET from {url}')
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f'Network exception occurred: {err}')
    return None


def analyze_review_sentiments(text):
    """Analyze the sentiment of a review text."""
    url = f'{SENTIMENT_ANALYZER_URL}analyze/{text}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as err:
        print(f'Error during sentiment analysis: {err}')
    return None


def post_review(data_dict):
    """Post a review payload to the backend."""
    url = f'{BACKEND_URL}/insert_review'
    try:
        response = requests.post(url, json=data_dict)
        response.raise_for_status()
        result = response.json()
        print(result)
        return result
    except requests.RequestException as err:
        print(f'Network exception occurred: {err}')
    return None
