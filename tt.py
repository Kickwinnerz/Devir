import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import os
import json
import logging

logging.basicConfig(level=logging.INFO)

def load_config():
    try:
        with open('config.json') as f:
            config = json.load(f)
            if 'page_id' not in config or 'access_token' not in config:
                logging.error("Error: config.json file is missing required keys")
                return None
            return config
    except FileNotFoundError:
        logging.error("Error: config.json file not found")
        return None
    except json.JSONDecodeError:
        logging.error("Error: config.json file is not valid JSON")
        return None

def get_followers_count(page_id, access_token):
    try:
        endpoint = f"https://graph.facebook.com/v13.0/{page_id}?fields=followers_count"
        params = {
            "access_token": access_token
        }
        session = requests.Session()
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        response = session.get(endpoint, params=params)
        response.raise_for_status()
        return response.json()["followers_count"]
    except requests.exceptions.RequestException as e:
        logging.error(f"Error: {e}")
        return None
    except KeyError:
        logging.error("Error: followers_count not found in response")
        return None

def main():
    config = load_config()
    if config:
        page_id = config["page_id"]
        access_token = config["access_token"]
        followers_count = get_followers_count(page_id, access_token)
        if followers_count:
            logging.info(f"Followers Count: {followers_count}")
        else:
            logging.error("Failed to retrieve followers count")

if __name__ == "__main__":
    main()