"""
Reddit Scraper Module
Handles scraping of Reddit user posts and comments
"""

import requests
import time
import logging
from typing import Dict, List
from datetime import datetime


class RedditScraper:
    """Scrapes Reddit user data including posts and comments."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.logger = logging.getLogger(__name__)
        
    def scrape_user_data(self, username: str) -> Dict:
        """
        Scrape posts and comments for a given Reddit user.
        
        Args:
            username: Reddit username
            
        Returns:
            Dictionary containing posts and comments data
        """
        user_data = {
            'username': username,
            'posts': [],
            'comments': []
        }
        
        # Scrape posts
        posts_url = f"https://www.reddit.com/user/{username}/submitted.json"
        user_data['posts'] = self._fetch_reddit_data(posts_url, 'posts')
        
        # Scrape comments
        comments_url = f"https://www.reddit.com/user/{username}/comments.json"
        user_data['comments'] = self._fetch_reddit_data(comments_url, 'comments')
        
        return user_data
    
    def _fetch_reddit_data(self, url: str, data_type: str) -> List[Dict]:
        """
        Fetch data from Reddit API endpoint.
        
        Args:
            url: Reddit API endpoint URL
            data_type: Type of data being fetched ('posts' or 'comments')
            
        Returns:
            List of processed Reddit items
        """
        items = []
        after = None
        max_pages = 10  # Limit to prevent excessive requests
        
        for page in range(max_pages):
            try:
                params = {'limit': 100}
                if after:
                    params['after'] = after
                
                response = self.session.get(url, params=params)
                response.raise_for_status()
                
                data = response.json()
                
                if not data.get('data', {}).get('children'):
                    break
                
                for item in data['data']['children']:
                    processed_item = self._process_item(item['data'], data_type)
                    if processed_item:
                        items.append(processed_item)
                
                after = data['data'].get('after')
                if not after:
                    break
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                self.logger.error(f"Error fetching {data_type}: {str(e)}")
                break
        
        self.logger.info(f"Fetched {len(items)} {data_type}")
        return items
    
    def _process_item(self, item_data: Dict, data_type: str) -> Dict:
        """
        Process individual Reddit item (post or comment).
        
        Args:
            item_data: Raw Reddit item data
            data_type: Type of item ('posts' or 'comments')
            
        Returns:
            Processed item dictionary
        """
        try:
            processed = {
                'id': item_data.get('id'),
                'created_utc': item_data.get('created_utc'),
                'score': item_data.get('score', 0),
                'subreddit': item_data.get('subreddit'),
                'permalink': f"https://reddit.com{item_data.get('permalink', '')}"
            }
            
            if data_type == 'posts':
                processed.update({
                    'title': item_data.get('title', ''),
                    'selftext': item_data.get('selftext', ''),
                    'url': item_data.get('url', ''),
                    'num_comments': item_data.get('num_comments', 0),
                    'post_hint': item_data.get('post_hint', ''),
                    'content': item_data.get('selftext', '') or item_data.get('title', '')
                })
            else:  # comments
                processed.update({
                    'body': item_data.get('body', ''),
                    'parent_id': item_data.get('parent_id', ''),
                    'link_title': item_data.get('link_title', ''),
                    'content': item_data.get('body', '')
                })
            
            return processed
            
        except Exception as e:
            self.logger.error(f"Error processing {data_type} item: {str(e)}")
            return None