#!/usr/bin/env python3
"""
Reddit User Persona Analyzer
Scrapes Reddit user data and generates persona using Gemini LLM
"""

import sys
import argparse
from pathlib import Path
from dotenv import load_dotenv

# Load .env before anything else
load_dotenv()

from reddit_scraper import RedditScraper
from persona_generator import PersonaGenerator
from utils import setup_logging, validate_reddit_url


def main():
    parser = argparse.ArgumentParser(description='Generate user persona from Reddit profile')
    parser.add_argument('profile_url', help='Reddit user profile URL')
    parser.add_argument('--output-dir', default='outputs', help='Output directory for results')
    args = parser.parse_args()

    logger = setup_logging()

    if not validate_reddit_url(args.profile_url):
        logger.error("Invalid Reddit profile URL provided")
        sys.exit(1)

    username = args.profile_url.rstrip('/').split('/')[-1]

    try:
        scraper = RedditScraper()
        persona_gen = PersonaGenerator()

        output_dir = Path(args.output_dir)
        output_dir.mkdir(exist_ok=True)

        logger.info(f"Starting analysis for user: {username}")

        logger.info("Scraping Reddit data...")
        user_data = scraper.scrape_user_data(username)

        if not user_data['posts'] and not user_data['comments']:
            logger.warning("No posts or comments found for this user")
            return

        logger.info("Generating user persona...")
        persona = persona_gen.generate_persona(user_data)

        output_file = output_dir / f"{username}_persona.txt"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(persona)

        logger.info(f"Persona saved to: {output_file}")
        print(f"User persona generated successfully: {output_file}")

    except Exception as e:
        logger.error(f"Error during execution: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
