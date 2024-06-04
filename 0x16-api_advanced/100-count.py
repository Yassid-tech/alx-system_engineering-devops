#!/usr/bin/python3
import requests

def count_words(subreddit, word_list, word_count={}, after=None):
    """Queries the Reddit API and returns the count of words in word_list in the titles of all the hot posts of the subreddit"""
    
    headers = {"User-Agent": "My-User-Agent"}
    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    params = {"after": after}
    
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)
    
    if response.status_code != 200:
        return
    
    data = response.json().get("data", {})
    children = data.get("children", [])
    
    if not children:
        return
    
    if not word_count:
        word_count = {word.lower(): 0 for word in word_list}
    
    for child in children:
        title = child.get("data", {}).get("title", "")
        title_words = title.split()
        for word in word_list:
            word_lower = word.lower()
            word_count[word_lower] += sum(1 for title_word in title_words if title_word.lower() == word_lower)
    
    after = data.get("after")
    
    if after:
        count_words(subreddit, word_list, word_count, after)
    else:
        sorted_word_count = sorted(word_count.items(), key=lambda kv: (-kv[1], kv[0]))
        for word, count in sorted_word_count:
            if count > 0:
                print(f"{word}: {count}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
        print("Ex: {} programming 'python java javascript'".format(sys.argv[0]))
    else:
        count_words(sys.argv[1], sys.argv[2].split())
