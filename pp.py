import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

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
        print(f"Error: {e}")
        return None
    except KeyError:
        print("Error: followers_count not found in response")
        return None

def main():
    page_id = "your-page-id"
    access_token = "your-page-access-token"
    followers_count = get_followers_count(page_id, access_token)
    if followers_count:
        print(f"Followers Count: {followers_count}")
    else:
        print("Failed to retrieve followers count")

if __name__ == "__main__":
    main()