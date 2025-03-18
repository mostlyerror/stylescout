# TikTok Fashion Scout Bot

A Python bot that searches for fashion videos on TikTok, identifies clothing items, and comments with Amazon affiliate links to similar products.

## Features

- Automatically finds trending fashion videos on TikTok
- Comments on videos with affiliate links to similar fashion items
- Uses Playwright for browser automation

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd <repository-directory>
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install dependencies:
   ```
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

5. Install Playwright browsers:
   ```
   python -m playwright install
   ```

## Configuration

Before running the bot, update the following settings in `bot.py`:

1. Set your Amazon affiliate tag:
   ```python
   AMAZON_AFFILIATE_TAG = "your-affiliate-tag"  # Replace with your actual tag
   ```

2. Customize the fashion items list or implement AI detection logic

## Usage

Run the bot with:
```
python bot.py
```

The bot will:
1. Search for fashion videos on TikTok
2. Identify fashion items in the videos 
3. Post comments with Amazon affiliate links

## Development

To contribute to the project:

1. Fork the repository
2. Create a feature branch
3. Uncomment and install development dependencies in requirements.txt
4. Submit a pull request

## License

[Specify your license here]

## Disclaimer

This bot is for educational purposes only. Make sure to comply with TikTok's terms of service and Amazon's affiliate program rules when using this bot.
