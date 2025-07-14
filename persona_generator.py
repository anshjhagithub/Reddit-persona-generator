"""
Persona Generator Module
Uses Gemini API to generate user personas from Reddit data
"""

import os
import json
import logging
from typing import Dict, List
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()


class PersonaGenerator:
    """Generates user personas using Gemini."""

    def __init__(self):
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not set in .env")
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('models/gemini-1.5-pro-latest')
        self.logger = logging.getLogger(__name__)

    def generate_persona(self, user_data: Dict) -> str:
        content_summary = self._prepare_content_for_analysis(user_data)
        persona_analysis = self._analyze_with_gemini(content_summary, user_data)
        return self._format_persona(persona_analysis, user_data)

    def _prepare_content_for_analysis(self, user_data: Dict) -> str:
        content_parts = []
        for post in user_data['posts'][:50]:
            if post.get('content'):
                content_parts.append(f"POST in r/{post.get('subreddit')}: {post['content']}")
        for comment in user_data['comments'][:100]:
            if comment.get('content'):
                content_parts.append(f"COMMENT in r/{comment.get('subreddit')}: {comment['content']}")
        return "\n\n".join(content_parts)

    def _analyze_with_gemini(self, content: str, user_data: Dict) -> Dict:
        prompt = f"""
Analyze the following Reddit user's posts and comments to create a comprehensive user persona.

User: {user_data['username']}

Content:
{content}

Please provide a detailed analysis in JSON format with the following structure:
{{
  "demographics": {{
    "age_range": "estimated age range",
    "location": "estimated location/region",
    "occupation": "estimated occupation or field"
  }},
  "interests": [
    "primary interests based on subreddit activity and content"
  ],
  "personality_traits": [
    "personality characteristics observed"
  ],
  "communication_style": "description of how they communicate",
  "values_beliefs": [
    "values and beliefs expressed"
  ],
  "lifestyle": "lifestyle indicators",
  "technical_expertise": "level of technical knowledge",
  "social_behavior": "online social behavior patterns"
}}
"""

        try:
            response = self.model.generate_content(
                [prompt],
                generation_config={
                    "temperature": 0.3,
                    "max_output_tokens": 2048
                }
            )

            text_response = response.text.strip()
            self.logger.info(f"Gemini raw response: {text_response[:200]}...")

            result = json.loads(text_response)
            return result

        except Exception as e:
            self.logger.error(f"Error with Gemini API: {str(e)}")
            return self._fallback_analysis(user_data)

    def _fallback_analysis(self, user_data: Dict) -> Dict:
        return {
            "demographics": {
                "age_range": "Unable to determine",
                "location": "Unable to determine",
                "occupation": "Unable to determine"
            },
            "interests": ["Based on subreddit activity"],
            "personality_traits": ["Active Reddit user"],
            "communication_style": "Engages in online discussions",
            "values_beliefs": ["Unable to determine without content analysis"],
            "lifestyle": "Active social media user",
            "technical_expertise": "Basic to intermediate",
            "social_behavior": "Participates in online communities"
        }

    def _format_persona(self, analysis: Dict, user_data: Dict) -> str:
        persona_text = f"""
USER PERSONA: {user_data['username']}
{'=' * 50}

DEMOGRAPHICS:
Age Range: {analysis['demographics']['age_range']}
Location: {analysis['demographics']['location']}
Occupation: {analysis['demographics']['occupation']}

INTERESTS:
{self._format_list(analysis['interests'])}

PERSONALITY TRAITS:
{self._format_list(analysis['personality_traits'])}

COMMUNICATION STYLE:
{analysis['communication_style']}

VALUES & BELIEFS:
{self._format_list(analysis['values_beliefs'])}

LIFESTYLE:
{analysis['lifestyle']}

TECHNICAL EXPERTISE:
{analysis['technical_expertise']}

SOCIAL BEHAVIOR:
{analysis['social_behavior']}

ANALYSIS SUMMARY:
Based on {len(user_data['posts'])} posts and {len(user_data['comments'])} comments.
Most active subreddits: {self._get_top_subreddits(user_data)}
"""
        return persona_text

    def _format_list(self, items: List[str]) -> str:
        return "\n".join(f"• {item}" for item in items)

    def _get_top_subreddits(self, user_data: Dict) -> str:
        subreddit_count = {}
        for post in user_data['posts']:
            sub = post.get('subreddit')
            if sub:
                subreddit_count[sub] = subreddit_count.get(sub, 0) + 1
        for comment in user_data['comments']:
            sub = comment.get('subreddit')
            if sub:
                subreddit_count[sub] = subreddit_count.get(sub, 0) + 1
        top_subs = sorted(subreddit_count.items(), key=lambda x: x[1], reverse=True)[:5]
        return ", ".join([f"r/{sub}" for sub, count in top_subs])
