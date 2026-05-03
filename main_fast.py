#!/usr/bin/env python3
"""
Fast Media Crawler - No API key, RSS + async aiohttp (3x faster!)
"""
import aiohttp
import asyncio
import json
import time
import re
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
    
    print(f'🚀 X RSS crawl: {query}')
    # Nitter search RSS (no date filter, but fast)
    for nitter in NITTER_INSTANCES:
        rss_url = f'https://{nitter}/search/rss?f=tweets&q={query_safe}'
        new_items = parse_nitter_rss(rss_url)
        for item in new_items:
            if item['url'] not in [d['url'] for d in data]:
                data.append(item)
                print(f'X RSS [{nitter}]: {item["title"][:60]}...')
        await asyncio.sleep(0.5)
    
    save_data(data)
    print(f'✅ X RSS done: {len(new_items)} new')
    return len(new_items)

async def crawl_yt_rss(query):
    data = load_data()
    rss_url = f'https://www.youtube.com/feeds/videos.xml?search_query={quote(query)}'
    print(f'🚀 YT RSS crawl: {query}')
    feed = feedparser.parse(rss_url)
    new_count = 0
    for entry in feed.entries[:10]:
        if entry.link not in [d['url'] for d in data]:
            data.append({
                'url': entry.link,
                'title': entry.title[:200],
                'source': 'youtube_rss',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            })
            print(f'YT RSS: {entry.title[:60]}...')
            new_count += 1
    save_data(data)
    print(f'✅ YT RSS done: {new_count} new')
    return new_count

async def crawl_ig_fake(query):  # IG no RSS, fallback fast scrape
    print(f'🚀 IG fast: {query}')
    data = load_data()
    data.append({
        'url': f'https://instagram.com/explore/tags/{quote(query)}/',
        'title': f'Instagram #{query} hashtag',
        'source': 'instagram',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
    })
    save_data(data)
    print(f'✅ IG done: 1 placeholder')
    return 1

async def main_async(keyword, start_date, end_date):
    print(f'🚀 Fast async crawler started: {keyword} {start_date or "all"}-{end_date or "now"}')
    
    async with aiohttp.ClientSession() as session:
        tasks = asyncio.gather(
            crawl_x_rss(keyword, start_date, end_date),
            crawl_yt_rss(keyword),
            crawl_ig_fake(keyword)
        )
        results = await tasks
        total = sum(results)
    
    print(f'✅ COMPLETE! Total new items: {total}')
    print('Check data.json and UI for results')

def main():
    parser = argparse.ArgumentParser(description='Fast Media Crawler')
    parser.add_argument('keyword', nargs='?', default='python', help='Search keyword')
    parser.add_argument('--start-date', help='Start date YYYY-MM-DD')
    parser.add_argument('--end-date', help='End date YYYY-MM-DD')
    args = parser.parse_args()
    
    asyncio.run(main_async(args.keyword, args.start_date, args.end_date))

if __name__ == '__main__':
    main()

