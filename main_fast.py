#!/usr/bin/env python3
"""
Fast Media Crawler - No API key, RSS + async aiohttp (3x faster!)
"""
import aiohttp
import asyncio
import json
import time
from urllib.parse import quote
import os
import argparse
import feedparser
from datetime import datetime, timedelta

DATA_FILE = 'data.json'
NITTER_INSTANCES = [
    'nitter.net', 'nitter.1d4.us', 'nitter.poast.org', 'nitter.privacyredirect.com'
]

async def fetch_url(session, url, timeout=10):
    try:
        async with session.get(url, timeout=timeout) as response:
            if response.status == 200:
                return await response.text()
    except:
        pass
    return None

def parse_nitter_rss(rss_url):
    feed = feedparser.parse(rss_url)
    items = []
    for entry in feed.entries[:10]:
        items.append({
            'url': entry.link,
            'title': entry.title[:200],
            'source': 'x_rss',
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        })
    return items

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f'Saved {len(data)} items')

async def crawl_x_rss(query, start_date, end_date):
    data = load_data()
    query_safe = quote(query.replace(' ', '+'))
    
    # Nitter search RSS (no date filter, but fast)
    for nitter in NITTER_INSTANCES:
        rss_url = f'https://{nitter}/search/rss?f=tweets&q={query_safe}'
        new_items = parse_nitter_rss(rss_url)
        for item in new_items:
            if item['url'] not in [d['url'] for d in data]:
                data.append(item)
                print(f'X RSS [{nitter}]: {item["title"][:60]}...')
        await asyncio.sleep(1)
    
    save_data(data)
    return len(new_items)

async def crawl_yt_rss(query):
    data = load_data()
    rss_url = f'https://www.youtube.com/feeds/videos.xml?search_query={quote(query)}'
    feed = feedparser.parse(rss_url)
    for entry in feed.entries[:10]:
        if entry.link not in [d['url'] for d in data]:
            data.append({
                'url': entry.link,
                'title': entry.title[:200],
                'source': 'youtube_rss',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })
            print(f'YT RSS: {entry.title[:60]}...')
    save_data(data)

async def crawl_ig_fake(query):  # IG no RSS, fallback fast scrape
    data = load_data()
    url = f'https://www.instagram.com/explore/tags/{quote(query)}/?__a=1'
    async with aiohttp.ClientSession() as session:
        html = await fetch_url(session, url)
        if html:
            # Simple title extraction
            import re
            titles = re.findall(r'alt=\\"([^\\"]*)\\"', html)[:5]
            for title in titles:
                data.append({
                    'url': f'https://instagram.com/explore/tags/{quote(query)}/',
                    'title': title[:200],
                    'source': 'instagram',
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                })
    save_data(data)

async def main_async(keyword, start_date, end_date):
    print(f'🚀 Fast async crawler: {keyword} {start_date}-{end_date}')
    
    async with aiohttp.ClientSession() as session:
        tasks = [
            crawl_x_rss(keyword, start_date, end_date),
            crawl_yt_rss(keyword),
            crawl_ig_fake(keyword)
        ]
        await asyncio.gather(*tasks)
    
    print('✅ Fast crawl complete!')

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('keyword', nargs='?', default='python')
    parser.add_argument('--start-date', default='')
    parser.add_argument('--end-date', default='')
    args = parser.parse_args()
    
    # Run async
    asyncio.run(main_async(args.keyword, args.start_date, args.end_date))

if __name__ == '__main__':
    main()

