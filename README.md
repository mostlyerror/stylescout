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

5. **IMPORTANT**: Install Playwright browsers:
   ```
   python -m playwright install
   ```
   This step is required to download the Chromium browser that the bot uses for automation. Without this step, the bot will fail to run.

6. Set up environment variables:
   ```
   cp .env.example .env
   ```
   Then edit the `.env` file with your actual configuration values.

## Configuration

The bot uses environment variables for configuration. Create a `.env` file in the project root with the following variables:

1. Set your Amazon affiliate tag:
   ```
   AMAZON_AFFILIATE_TAG=your-actual-affiliate-tag
   ```

2. Customize the fashion items list or implement AI detection logic in `bot.py`

## Usage

Run the bot with:
```
python bot.py
```

The bot will:
1. Search for fashion videos on TikTok
2. Identify fashion items in the videos 
3. Post comments with Amazon affiliate links

## Troubleshooting

### Common Issues

1. **"Browser not found" error**
   - Solution: Make sure you've run `python -m playwright install` as described in step 5 of the installation process
   - This command downloads the necessary browser binaries for Playwright

2. **"Playwright not found" error**
   - Solution: Make sure you've activated your virtual environment and installed all requirements with `pip install -r requirements.txt`

3. **Browser launch issues**
   - Make sure you have sufficient permissions in your working directory
   - Check if your antivirus software is blocking Playwright's browser launch

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
