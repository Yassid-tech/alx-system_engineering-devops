#!/usr/bin/python3
"""Function to query subscribers on a given Reddit subreddit."""
import requests


def number_of_subscribers(subreddit):
    """Return the total number of subscribers on a given subreddit."""
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    try:
        response = requests.get(url, headers=headers, allow_redirects=False)
        if response.status_code == 200:
            try:
                results = response.json().get("data")
                return results.get("subscribers", 0)
            except ValueError:
                print("Error: Unable to parse JSON response")
                return 0
        elif response.status_code == 404:
            print("Error: Subreddit not found")
            return 0
        else:
            print(f"Error: HTTP status code {response.status_code}")
            return 0
    except requests.RequestException as e:
        print(f"HTTP Request failed: {e}")
        return 0
