# TikTok Fashion Scout Bot

A Python bot that searches for fashion videos on TikTok, identifies clothing items, and comments with Amazon affiliate links to similar products.

## Features

- Automatically finds trending fashion videos on TikTok
- Comments on videos with affiliate links to similar fashion items
- Uses Playwright for browser automation
- Handles TikTok authentication automatically
- Persists login state to avoid repeated captcha solving
- Debug logging for troubleshooting

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Git
- TikTok account with commenting permissions
- Amazon Associates account

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

2. Set your TikTok login credentials:
   ```
   TIKTOK_USERNAME=your-tiktok-username
   TIKTOK_PASSWORD=your-tiktok-password
   ```
   Note: Make sure your TikTok account has commenting permissions and is in good standing.

3. Configure bot behavior (optional):
   ```
   MIN_DELAY_SECONDS=45
   MAX_DELAY_SECONDS=75
   ```

4. Customize the fashion items list or implement AI detection logic in `bot.py`

## Usage

1. First run (with visible browser to handle captcha):
   ```bash
   python bot.py --visible
   ```
   > **Note**: The `--visible` flag is required for the first run or when you need to solve a captcha. You need to be able to see and interact with the browser window to solve the captcha manually. After the first successful login, you can run the bot headlessly since it will use the saved authentication state.

2. Subsequent runs (can run headless):
   ```bash
   python bot.py
   ```

3. If you need to force a new login:
   ```bash
   python bot.py --force-login
   ```

4. Enable debug logging:
   ```bash
   python bot.py --debug
   ```

The bot will:
1. Log in to your TikTok account (or use saved authentication state)
2. Search for fashion videos on TikTok
3. Identify fashion items in the videos 
4. Post comments with Amazon affiliate links

### Authentication State

The bot saves your TikTok authentication state after a successful login. This means:
- You only need to solve captchas once during the first login
- Subsequent runs will reuse the saved authentication
- If the saved authentication expires, the bot will automatically perform a new login
- Use `--force-login` if you need to perform a fresh login

### Debug Logging

The bot includes a comprehensive debug logging system with three levels that can be enabled with the `--debug` flag:

```bash
# No debug output (default)
python bot.py

# Basic debug output (level 1)
python bot.py --debug 1

# Verbose debug output (level 2)
python bot.py --debug 2
```

Debug levels:
- Level 0 (default): Shows only essential operational logs
- Level 1 (basic): Shows additional operational information including:
  - Browser state changes
  - Login flow steps
  - Network activity
  - Configuration details
- Level 2 (verbose): Shows detailed debugging information including:
  - Page element information
  - Form field details
  - DOM structure
  - All available elements and their attributes

Debug logs are particularly useful when:
- Troubleshooting login issues
- Investigating why elements aren't being found
- Understanding the bot's behavior
- Diagnosing network or timing problems

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
   - Try running in visible mode with `--visible` flag to see what's happening

4. **Login issues**
   - Verify your TikTok credentials in the .env file
   - Try running in visible mode (`--visible` flag) to see the login process
   - If you see a captcha, run in visible mode and solve it manually
   - If login fails, try using `--force-login` to perform a fresh login
   - Make sure your TikTok account is not locked or restricted

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
