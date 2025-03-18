from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import requests
import time
from dotenv import load_dotenv
import os
import random
from datetime import datetime
import argparse

# Load environment variables
load_dotenv()

# Parse command line arguments
parser = argparse.ArgumentParser(description='TikTok Fashion Scout Bot')
parser.add_argument('--visible', action='store_true', help='Run browser in visible mode (useful for debugging)')
parser.add_argument('--force-login', action='store_true', help='Force new login, ignoring saved state')
args = parser.parse_args()

# Configuration
AMAZON_AFFILIATE_TAG = os.getenv('AMAZON_AFFILIATE_TAG')
TIKTOK_USERNAME = os.getenv('TIKTOK_USERNAME')
TIKTOK_PASSWORD = os.getenv('TIKTOK_PASSWORD')

# Storage state configuration
STORAGE_STATE_DIR = "auth_state"
STORAGE_STATE_PATH = os.path.join(STORAGE_STATE_DIR, "tiktok_auth.json")

# Validate required environment variables
if not AMAZON_AFFILIATE_TAG:
    raise ValueError("AMAZON_AFFILIATE_TAG not found in environment variables. Please check your .env file.")
if not TIKTOK_USERNAME or not TIKTOK_PASSWORD:
    raise ValueError("TIKTOK_USERNAME and TIKTOK_PASSWORD must be set in your .env file.")

# Bot behavior configuration
MIN_DELAY = int(os.getenv('MIN_DELAY_SECONDS', '45'))
MAX_DELAY = int(os.getenv('MAX_DELAY_SECONDS', '75'))

def get_random_delay():
    """Generate a random delay between comments to simulate human-like behavior."""
    return random.randint(MIN_DELAY, MAX_DELAY)

def log_action(message):
    """Print a timestamped action message."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def handle_tiktok_login(page, context):
    """Handle TikTok login process."""
    log_action("Checking if login is required...")
    
    try:
        # Wait for either the login form or the search results
        login_button = page.wait_for_selector("button:has-text('Log in')", timeout=5000)
        if login_button:
            log_action("Login required. Attempting to log in...")
            
            # Click the login button
            login_button.click()
            
            # Wait for and fill in the login form
            page.wait_for_selector("input[name='username']")
            page.fill("input[name='username']", TIKTOK_USERNAME)
            page.fill("input[name='password']", TIKTOK_PASSWORD)
            
            # Click the login button
            page.click("button:has-text('Log in')")
            
            # Check for captcha
            captcha_frame = page.frame_locator('iframe[title*="captcha"]')
            if captcha_frame:
                print("Captcha detected! Please solve it manually...")
                # Wait for captcha to be solved (frame disappears)
                page.wait_for_selector('iframe[title*="captcha"]', state='detached', timeout=300000)
            
            # Wait for login to complete
            try:
                page.wait_for_selector("input[type='search']", timeout=10000)
                log_action("Successfully logged in to TikTok")
                
                # Save storage state after successful login
                if not os.path.exists(STORAGE_STATE_DIR):
                    os.makedirs(STORAGE_STATE_DIR)
                context.storage_state(path=STORAGE_STATE_PATH)
                log_action("Saved authentication state for future use")
                
                return True
            except PlaywrightTimeoutError:
                log_action("Login might have failed or requires additional verification")
                return False
                
    except PlaywrightTimeoutError:
        log_action("No login required or already logged in")
        return True

def get_browser_context(playwright):
    """Get a browser context with optional storage state."""
    browser = playwright.chromium.launch(headless=not args.visible)
    
    # Try to load storage state if it exists and force-login is not set
    if os.path.exists(STORAGE_STATE_PATH) and not args.force_login:
        log_action("Loading saved authentication state...")
        context = browser.new_context(storage_state=STORAGE_STATE_PATH)
    else:
        log_action("Creating new browser context...")
        context = browser.new_context()
    
    return browser, context

# Amazon affiliate API (placeholder function)
def search_amazon_product(query):
    log_action(f"Generating Amazon affiliate link for: {query}")
    return f"https://www.amazon.com/s?k={query.replace(' ', '+')}&tag={AMAZON_AFFILIATE_TAG}"

# TikTok automation to find fashion videos
def get_fashion_videos():
    log_action("Starting TikTok search for fashion videos...")
    with sync_playwright() as p:
        browser, context = get_browser_context(p)
        page = context.new_page()
        
        # Go to TikTok and handle login
        page.goto("https://www.tiktok.com")
        if not handle_tiktok_login(page, context):
            raise Exception("Failed to log in to TikTok. Please check your credentials and try again.")
        
        # Navigate to search
        page.goto("https://www.tiktok.com/search?q=fashion")
        
        log_action("Waiting for search results to load...")
        try:
            page.wait_for_selector("a[href*='/video/']", timeout=10000)
        except PlaywrightTimeoutError:
            log_action("No videos found in search results")
            return []

        video_links = page.eval_on_selector_all("a[href*='/video/']", "elements => elements.map(el => el.href)")
        browser.close()
        log_action(f"Found {len(video_links)} fashion videos")
        return video_links[:3]  # Fetch top 3 videos

# Post a comment on the video
def comment_on_video(video_url, message):
    log_action(f"Processing video: {video_url}")
    with sync_playwright() as p:
        browser, context = get_browser_context(p)
        page = context.new_page()
        
        # Go to TikTok and handle login
        page.goto("https://www.tiktok.com")
        if not handle_tiktok_login(page, context):
            raise Exception("Failed to log in to TikTok. Please check your credentials and try again.")
            
        page.goto(video_url)

        # Wait for comment box
        log_action("Waiting for comment box to load...")
        try:
            page.wait_for_selector("textarea[data-e2e='comment-text-area']", timeout=10000)
        except PlaywrightTimeoutError:
            log_action("Could not find comment box. Video might require login or be unavailable.")
            browser.close()
            return False

        page.fill("textarea[data-e2e='comment-text-area']", message)
        log_action("Posting comment...")
        page.click("button[data-e2e='comment-post']")

        browser.close()
        log_action("Comment posted successfully")
        return True

# Main execution
log_action("Starting TikTok Fashion Scout Bot...")
log_action(f"Using Amazon affiliate tag: {AMAZON_AFFILIATE_TAG}")
log_action(f"Running in {'visible' if args.visible else 'headless'} mode")
if args.force_login:
    log_action("Force login enabled - will perform fresh login")

try:
    videos = get_fashion_videos()
    if not videos:
        log_action("No videos found. Exiting...")
        exit(1)

    log_action(f"Processing {len(videos)} videos...")

    for index, video in enumerate(videos, 1):
        log_action(f"\nProcessing video {index} of {len(videos)}")
        fashion_items = ["Nike Shoes", "Adidas Hoodie"]  # Replace with AI detection logic
        log_action(f"Detected fashion items: {', '.join(fashion_items)}")
        
        product_links = [search_amazon_product(item) for item in fashion_items]
        comment_text = f"Love this look! Get similar styles here: {', '.join(product_links)} #fashion"
        
        if not comment_on_video(video, comment_text):
            log_action(f"Skipping remaining videos due to error with video {index}")
            break

        if index < len(videos):  # Don't delay after the last video
            delay = get_random_delay()
            log_action(f"Waiting {delay} seconds before next comment...")
            time.sleep(delay)

    log_action("\nBot completed successfully!")

except Exception as e:
    log_action(f"Error occurred: {str(e)}")
    exit(1)
