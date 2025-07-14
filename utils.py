"""
Utility Functions
Common helper functions for the Reddit persona analyzer
"""

import logging
import re
from typing import Optional  # Keep other type hints if needed

def setup_logging() -> logging.Logger:
    """
    Setup logging configuration.
    
    Returns:
        Configured logger instance
    """
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('reddit_analyzer.log'),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def validate_reddit_url(url: str) -> bool:
    """
    Validate if the provided URL is a valid Reddit user profile URL.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid Reddit user URL, False otherwise
    """
    reddit_user_pattern = r'^https?://(?:www\.)?reddit\.com/user/[^/]+/?$'
    return bool(re.match(reddit_user_pattern, url))

def extract_username_from_url(url: str) -> str:
    """
    Extract username from Reddit profile URL.
    
    Args:
        url: Reddit profile URL
        
    Returns:
        Username string
    """
    # Remove trailing slash if present
    url = url.rstrip('/')
    
    # Extract username from URL
    parts = url.split('/')
    if len(parts) >= 2 and parts[-2] == 'user':
        return parts[-1]
    
    return ""

def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to remove invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename
    """
    # Remove invalid characters for filenames
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    return filename

def truncate_text(text: str, max_length: int = 1000) -> str:
    """
    Truncate text to specified maximum length.
    
    Args:
        text: Text to truncate
        max_length: Maximum length allowed
        
    Returns:
        Truncated text
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length] + "..."

def format_timestamp(timestamp: float) -> str:
    """
    Format Unix timestamp to readable date string.
    
    Args:
        timestamp: Unix timestamp
        
    Returns:
        Formatted date string
    """
    from datetime import datetime
    
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, OSError):
        return "Unknown date"

def clean_reddit_content(content: str) -> str:
    """
    Clean Reddit content by removing markdown and special characters.
    
    Args:
        content: Raw Reddit content
        
    Returns:
        Cleaned content
    """
    if not content:
        return ""
    
    # Remove Reddit markdown
    content = re.sub(r'\*\*(.*?)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*(.*?)\*', r'\1', content)      # Italic
    content = re.sub(r'~~(.*?)~~', r'\1', content)      # Strikethrough
    content = re.sub(r'\^(.*?)\^', r'\1', content)      # Superscript
    content = re.sub(r'&gt;!(.+?)!&lt;', r'\1', content)  # Spoiler
    content = re.sub(r'&gt;', '>', content)             # Quote
    content = re.sub(r'&lt;', '<', content)             # Less than
    content = re.sub(r'&amp;', '&', content)            # Ampersand
    
    # Remove URLs
    content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', 
                    '[URL]', content)
    
    # Remove excessive whitespace
    content = re.sub(r'\s+', ' ', content).strip()
    
    return content