#!/usr/bin/env python3
"""
Social Media Crawler - File-based (no DB needed)
Crawls Twitter/X, Instagram, YouTube → saves to data.json
"""
import requests
from bs4 import BeautifulSoup
import json
import time
import random
from urllib.parse import urlparse
import re
import os

DATA_FILE = 'data.json'

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
]

def get_headers():
    return {
        'User-Agent': random.choice(USER_AGENTS),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Saved {len(data)} items to {DATA_FILE}')

def crawl_twitter_search(query, max_pages=2):
    data = load_data()
    base_url = 'https://twitter.com/search?q=' + requests.utils.quote(query) + '&src=typed_query'
    
    for page in range(max_pages):
        url = base_url + f'&f=live' if page == 0 else f'{base_url}&p={page+1}'
        try:
            response = requests.get(url, headers=get_headers(), timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            tweets = soup.find_all('article', {'data-testid': 'tweet'})
            
            for tweet in tweets:
                link = tweet.find('a', href=re.compile(r'/[^/]+/status/'))
                if link:
                    tweet_url = 'https://twitter.com' + link['href']
                    if tweet_url not in [item['url'] for item in data]:
                        title = tweet.get_text()[:200].strip()
                        data.append({
                            'url': tweet_url,
                            'title': title,
                            'source': 'twitter',
                            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                        })
                        print(f'Twitter [{query}]: {tweet_url}')
            time.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f'Twitter error: {e}')
    
    save_data(data)
    print(f'Twitter crawl complete for "{query}"')

def crawl_instagram_explore(query, max_items=10):
    data = load_data()
    url = f'https://www.instagram.com/explore/tags/{requests.utils.quote(query)}/'
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        posts = soup.find_all('a', href=re.compile(r'/p/'))
        
        for post in posts[:max_items]:
            post_url = 'https://www.instagram.com' + post['href']
            if post_url not in [item['url'] for item in data]:
                title = post.get('title', post.get_text()[:100]).strip()
                data.append({
                    'url': post_url,
                    'title': title,
                    'source': 'instagram',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f'Instagram [{query}]: {post_url}')
        
        save_data(data)
    except Exception as e:
        print(f'Instagram error: {e}')

def crawl_youtube_search(query, max_videos=10):
    data = load_data()
    url = f'https://www.youtube.com/results?search_query={requests.utils.quote(query)}'
    
    try:
        response = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        videos = soup.find_all('a', href=re.compile(r'/watch\?v='))
        
        for video in videos[:max_videos]:
            video_url = 'https://youtube.com' + video['href']
            if video_url not in [item['url'] for item in data]:
                title_tag = video.find('yt-formatted-string')
                title = title_tag.get_text().strip() if title_tag else video.get_text()[:100]
                data.append({
                    'url': video_url,
                    'title': title,
                    'source': 'youtube',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
                print(f'YouTube [{query}]: {video_url}')
        
        save_data(data)
    except Exception as e:
        print(f'YouTube error: {e}')

def main():
    print("Social Media Crawler starting... (no DB - saves to data.json)")
    
    # Crawl social media
    crawl_twitter_search('python programming', 1)
    crawl_instagram_explore('coding', 5)
    crawl_youtube_search('python tutorial', 10)
    
    print("All done! Check data.json")

if __name__ == '__main__':
    main()

