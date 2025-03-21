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
parser.add_argument('--debug', type=int, default=0, choices=[0, 1, 2], help='Debug level (0: none, 1: basic, 2: verbose)')
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

def log_action(message, debug_level=0):
    """Print a timestamped action message.
    
    Args:
        message: The message to log
        debug_level: Debug level (0: normal log, 1: basic debug, 2: verbose debug)
    """
    if debug_level > 0 and args.debug < debug_level:
        return
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    prefix = ""
    if debug_level == 1:
        prefix = "[DEBUG] "
    elif debug_level == 2:
        prefix = "[DEBUG2] "
    print(f"[{timestamp}] {prefix}{message}", flush=True)

# Test log at script start
log_action("Script started")
log_action(f"Debug level: {args.debug}", debug_level=1)

# Main execution
log_action("Starting TikTok Fashion Scout Bot...")
log_action(f"Using Amazon affiliate tag: {AMAZON_AFFILIATE_TAG}")
log_action(f"Running in {'visible' if args.visible else 'headless'} mode", debug_level=1)
if args.force_login:
    log_action("Force login enabled - will perform fresh login", debug_level=1)

def clear_auth_state():
    """Clear the saved authentication state."""
    if os.path.exists(STORAGE_STATE_PATH):
        try:
            os.remove(STORAGE_STATE_PATH)
            log_action("Cleared saved authentication state")
        except Exception as e:
            log_action(f"Error clearing auth state: {str(e)}")

def handle_tiktok_login(page, context):
    """Handle TikTok login process."""
    log_action("Checking login state...")
    
    try:
        # First check if we're already logged in by looking for the search bar
        log_action("Checking if already logged in...")
        page.evaluate("""
            const searchBar = document.querySelector('input[type="search"]');
            if (!searchBar) {
                throw new Error('Search bar not found - not logged in');
            }
        """)
        log_action("Found search bar - already logged in")
        return True
    except Exception:
        log_action("Not logged in - proceeding with login flow")
    
    # If we get here, we need to log in
    log_action("Attempting to log in...")
    
    try:
        # Wait for and click the login button
        log_action("Looking for login button...")
        # Wait for page to be fully loaded
        page.wait_for_load_state('networkidle')
        
        # Check if login button exists
        page.evaluate("""
            const button = document.querySelector('#header-login-button');
            if (!button) {
                throw new Error('Login button not found');
            }
        """)
        
        log_action("Found login button, attempting to click...")
        page.evaluate("document.querySelector('#header-login-button').click()")
        
        # Wait for and click the "Use phone / email / username" button
        log_action("Waiting for login options to appear...")
        page.wait_for_load_state('networkidle')
        
        # Add a small delay to let the modal appear
        time.sleep(2)
        
        # Debug: Log all elements with class names
        log_action("Debugging page elements...", debug_level=2)
        elements = page.evaluate("""
            const elements = document.querySelectorAll('*');
            const elementInfo = [];
            elements.forEach(el => {
                elementInfo.push({
                    tag: el.tagName,
                    class: el.className,
                    id: el.id,
                    text: el.textContent.trim()
                });
            });
            // Use the variable in subsequent code
            const debugInfo = {
                totalElements: elementInfo.length,
                elements: elementInfo
            };
            debugInfo;
        """)
        log_action(f"Found elements: {elements}", debug_level=2)
        
        # Wait for the login modal to appear and get its content
        log_action("Waiting for login modal...")
        modal_content = page.evaluate("""
            const modal = document.querySelector('[role="dialog"][aria-modal="true"][data-e2e="login-modal"]');
            if (!modal) {
                throw new Error('Login modal not found');
            }
            
            const loginOptions = modal.querySelectorAll('[role="link"][data-e2e="channel-item"]');
            const optionTexts = [];
            loginOptions.forEach(option => optionTexts.push(option.textContent.trim()));
            
            // Assign to a variable that will be returned
            const result = {
                optionCount: optionTexts.length,
                options: optionTexts
            };
            result;
        """)
        log_action(f"Login options in modal: {modal_content}", debug_level=2)
        
        # Try to find and click the login option within the modal
        log_action("Looking for login option...")
        page.evaluate("""
            const modal = document.querySelector('[role="dialog"][aria-modal="true"][data-e2e="login-modal"]');
            if (!modal) {
                throw new Error('Login modal not found');
            }
            
            const loginOptions = modal.querySelectorAll('[role="link"][data-e2e="channel-item"]');
            let targetOption = null;
            loginOptions.forEach(option => {
                if (option.textContent.trim().includes('Use phone / email / username')) {
                    targetOption = option;
                }
            });
            if (!targetOption) {
                throw new Error('Could not find "Use phone / email / username" option in modal');
            }
            targetOption.click();
        """)
        
        # Wait for and click the "Log in with email or username" link
        log_action("Waiting for email login option...")
        page.wait_for_load_state('networkidle')
        log_action("Clicking 'Log in with email or username' link...")
        page.evaluate("""
            const links = document.querySelectorAll('a');
            let targetLink = null;
            links.forEach(link => {
                if (link.textContent.trim().includes('Log in with email or username')) {
                    targetLink = link;
                }
            });
            if (!targetLink) {
                throw new Error('Could not find "Log in with email or username" link');
            }
            targetLink.click();
        """)
        
        # Wait for and fill in the login form
        log_action("Waiting for login form...")
        # Wait for network to be idle after clicking the link
        page.wait_for_load_state('networkidle')
        # Add a small delay to let the form appear
        time.sleep(2)
        
        # Debug: Log all form elements
        log_action("Debugging form elements...", debug_level=2)
        form_elements = page.evaluate("""
            const forms = document.querySelectorAll('form');
            const inputs = document.querySelectorAll('input');
            const formInfo = {
                formCount: forms.length,
                forms: Array.from(forms).map(form => ({
                    id: form.id,
                    class: form.className,
                    action: form.action
                })),
                inputCount: inputs.length,
                inputs: Array.from(inputs).map(input => ({
                    type: input.type,
                    name: input.name,
                    id: input.id,
                    class: input.className,
                    placeholder: input.placeholder
                }))
            };
            formInfo;
        """)
        log_action(f"Form elements found: {form_elements}", debug_level=2)
        
        log_action("Filling in login credentials...")
        page.evaluate(f"""
            const usernameInput = document.querySelector('input[type="text"][placeholder="Email or username"]');
            const passwordInput = document.querySelector('input[type="password"][placeholder="Password"]');
            if (!usernameInput || !passwordInput) {{
                throw new Error('Could not find login form inputs');
            }}
            usernameInput.value = '{TIKTOK_USERNAME}';
            passwordInput.value = '{TIKTOK_PASSWORD}';
        """)
        
        # Click the login button
        log_action("Submitting login form...")
        page.evaluate("""
            const modal = document.querySelector('[role="dialog"][aria-modal="true"][data-e2e="login-modal"]');
            if (!modal) {
                throw new Error('Login modal not found');
            }
            
            const loginButton = modal.querySelector('button[type="submit"][data-e2e="login-button"]');
            if (!loginButton) {
                throw new Error('Could not find login submit button');
            }
            loginButton.click();
        """)
        
        # Check for captcha
        log_action("Checking for captcha...")
        try:
            page.evaluate("""
                const captchaFrame = document.querySelector('iframe[title*="captcha"]');
                if (captchaFrame) {
                    throw new Error('Captcha detected');
                }
            """)
        except Exception as e:
            if "Captcha detected" in str(e):
                log_action("Captcha detected! Please solve it manually...")
                log_action("Waiting for captcha to be solved...")
                
                # Clear auth state when captcha is detected
                clear_auth_state()
                
                # Wait for captcha to be solved (check every 2 seconds)
                max_wait = 300  # 5 minutes max wait
                start_time = time.time()
                while time.time() - start_time < max_wait:
                    try:
                        # Check if captcha is still present
                        page.evaluate("""
                            const captchaFrame = document.querySelector('iframe[title*="captcha"]');
                            if (captchaFrame) {
                                throw new Error('Captcha still present');
                            }
                        """)
                        log_action("Captcha solved! Continuing...")
                        break
                    except Exception:
                        if time.time() - start_time >= max_wait:
                            log_action("Timeout waiting for captcha to be solved")
                            return False
                        time.sleep(2)
            else:
                raise e
        
        # Wait for login to complete
        try:
            log_action("Waiting for login to complete...")
            page.evaluate("""
                const searchBar = document.querySelector('input[type="search"]');
                if (!searchBar) {
                    throw new Error('Login might have failed - search bar not found');
                }
            """)
            log_action("Successfully logged in to TikTok")
            
            # Save storage state after successful login
            if not os.path.exists(STORAGE_STATE_DIR):
                os.makedirs(STORAGE_STATE_DIR)
            context.storage_state(path=STORAGE_STATE_PATH)
            log_action("Saved authentication state for future use")
            
            return True
        except Exception as e:
            log_action(f"Login might have failed: {str(e)}")
            clear_auth_state()  # Clear auth state on login failure
            return False
            
    except Exception as e:
        log_action(f"Login error: {str(e)}")
        clear_auth_state()  # Clear auth state on any login error
        return False

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
    log_action(f"Generating Amazon affiliate link for: {query}", debug_level=2)
    return f"https://www.amazon.com/s?k={query.replace(' ', '+')}&tag={AMAZON_AFFILIATE_TAG}"

# TikTok automation to find fashion videos
def get_fashion_videos():
    log_action("Starting TikTok search for fashion videos...")
    with sync_playwright() as p:
        log_action("Initialized Playwright...", debug_level=2)
        browser, context = get_browser_context(p)
        log_action("Got browser context...", debug_level=2)
        page = context.new_page()
        log_action("Created new page...", debug_level=2)
        
        # Go to TikTok and handle login
        log_action("Navigating to TikTok...")
        page.goto("https://www.tiktok.com")
        if not handle_tiktok_login(page, context):
            raise Exception("Failed to log in to TikTok. Please check your credentials and try again.")
        
        # Use the search bar instead of direct navigation
        log_action("Using search bar to find fashion videos...")
        page.evaluate("""
            const searchBar = document.querySelector('input[type="search"]');
            if (!searchBar) {
                throw new Error('Search bar not found');
            }
            searchBar.value = 'fashion';
            searchBar.dispatchEvent(new Event('input', { bubbles: true }));
            searchBar.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', keyCode: 13, which: 13, bubbles: true }));
        """)
        
        # Wait for search results to load
        log_action("Waiting for search results to load...")
        page.wait_for_load_state('networkidle')
        time.sleep(3)  # Additional delay for results to render
        
        # Try to find video links with a timeout
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                log_action(f"Attempt {attempt + 1}/{max_attempts}: Searching for video links...", debug_level=2)
                
                # Debug: Log all links on the page
                page.evaluate("""
                    const allLinks = document.querySelectorAll('a');
                    const linkInfo = Array.from(allLinks).map(link => ({
                        href: link.href,
                        text: link.textContent.trim(),
                        isVideo: link.href.includes('/video/')
                    }));
                    linkInfo;
                """)
                
                # Try to find video links
                page.evaluate("""
                    const videoLinks = document.querySelectorAll('a[href*="/video/"]');
                    if (!videoLinks.length) {
                        throw new Error('No videos found in search results');
                    }
                """)
                
                # Debug: Log the number of video links found
                video_count = page.evaluate("""
                    document.querySelectorAll('a[href*="/video/"]').length;
                """)
                log_action(f"Found {video_count} video links in search results...", debug_level=2)
                break
                
            except Exception as e:
                if attempt == max_attempts - 1:
                    log_action(f"No videos found after {max_attempts} attempts: {str(e)}")
                    return []
                log_action(f"Attempt {attempt + 1}/{max_attempts}: Waiting for videos to load...", debug_level=1)
                log_action(f"Error on attempt {attempt + 1}: {str(e)}", debug_level=2)
                time.sleep(2)  # Wait 2 seconds between attempts

        video_links = page.evaluate("""
            const links = document.querySelectorAll('a[href*="/video/"]');
            const hrefs = [];
            links.forEach(link => hrefs.push(link.href));
            
            // Use the variable in subsequent code
            const videoInfo = {
                totalVideos: hrefs.length,
                links: hrefs
            };
            videoInfo;
        """)
        log_action(f"Extracted {len(video_links.get('links', []))} video links...", debug_level=2)
        browser.close()
        log_action("Closed browser...", debug_level=2)
        return video_links.get('links', [])[:3]  # Fetch top 3 videos

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
            page.evaluate("""
                const commentBox = document.querySelector('textarea[data-e2e="comment-text-area"]');
                if (!commentBox) {
                    throw new Error('Comment box not found');
                }
            """)
        except Exception as e:
            log_action(f"Could not find comment box: {str(e)}")
            browser.close()
            return False

        page.evaluate(f"""
            const commentBox = document.querySelector('textarea[data-e2e="comment-text-area"]');
            commentBox.value = '{message}';
        """)
        log_action("Posting comment...")
        page.evaluate("""
            const postButton = document.querySelector('button[data-e2e="comment-post"]');
            if (!postButton) {
                throw new Error('Comment post button not found');
            }
            postButton.click();
        """)

        browser.close()
        log_action("Comment posted successfully", debug_level=2)
        return True

try:
    # Get fashion videos
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
