# Reddit User Persona Analyzer

A Python script that analyzes Reddit user profiles to generate comprehensive user personas using AI-powered analysis.

Note : Please use your own API key in the .env file is provided (set GEMINI_API_KEY=YOUR KEY ) and sample outputs are also provided

## Features

- Scrapes Reddit user posts and comments
- Generates detailed user personas using Gemini AI API
- Provides citations for persona characteristics
- Clean, modular code structure
- Comprehensive error handling and logging

## Setup Instructions

### 1. Prerequisites

- Python 3.7 or higher


### 2. Installation

```bash
# Clone the repository
git clone <your-repo-url>
cd reddit-persona-analyzer

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your Groq API key
```

### 3. Configuration

Edit the `.env` file and add your Gemini API key:

```
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

## Usage

### Basic Usage

```bash
python main.py https://www.reddit.com/user/username/
```

### With Custom Output Directory

```bash
python main.py https://www.reddit.com/user/username/ --output-dir custom_output
```

### Examples

Analyze the sample users from the assignment:

```bash
python main.py https://www.reddit.com/user/kojied/
python main.py https://www.reddit.com/user/Hungry-Move-6603/
```

## Output

The script generates a detailed persona file in the specified output directory (default: `outputs/`) with the following structure:

- Demographics (age range, location, occupation)
- Interests and hobbies
- Personality traits
- Communication style
- Values and beliefs
- Lifestyle indicators
- Technical expertise level
- Social behavior patterns
- Supporting evidence with citations

## Project Structure

```
reddit-persona-analyzer/
├── main.py                 # Main execution script
├── reddit_scraper.py       # Reddit data scraping module
├── persona_generator.py    # AI persona generation module
├── utils.py               # Utility functions
├── requirements.txt       # Python dependencies
├── .env.example          # Environment variables template
├── README.md             # This file
└── outputs/              # Generated persona files
```

## Technical Details

### Reddit Data Scraping

- Uses Reddit's JSON API endpoints
- Implements rate limiting to respect API guidelines
- Handles pagination for comprehensive data collection
- Processes both posts and comments

### AI Analysis

- Powered by Gemini's 1.5 pro model
- Analyzes content patterns and language use
- Generates structured persona characteristics
- Provides evidence-based insights

### Error Handling

- Comprehensive logging system
- Graceful failure recovery
- Input validation
- API error handling

## Dependencies

- `requests`: HTTP requests for Reddit API
- `gemini`: Gemini AI API client
- `python-dotenv`: Environment variable management

## Limitations

- Requires public Reddit profiles
- Limited by Reddit's rate limiting
- Analysis quality depends on available user content
- Gemini API rate limits may apply

## Contributing

1. Follow PEP-8 style guidelines
2. Add comprehensive docstrings
3. Include error handling
4. Test with multiple user profiles

## License

This project is created for educational purposes 