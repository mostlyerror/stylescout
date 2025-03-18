from playwright.sync_api import sync_playwright
import requests
import time

# Amazon affiliate tag configuration
AMAZON_AFFILIATE_TAG = "your-affiliate-tag"

# Amazon affiliate API (placeholder function)
def search_amazon_product(query):
    return f"https://www.amazon.com/s?k={query.replace(' ', '+')}&tag={AMAZON_AFFILIATE_TAG}"

# TikTok automation to find fashion videos
def get_fashion_videos():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)  
        page = browser.new_page()
        page.goto("https://www.tiktok.com/search?q=fashion")

        video_links = page.eval_on_selector_all("a[href*='/video/']", "elements => elements.map(el => el.href)")
        browser.close()
        return video_links[:3]  # Fetch top 3 videos

# Post a comment on the video
def comment_on_video(video_url, message):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(video_url)

        # Wait for comment box
        page.wait_for_selector("textarea[data-e2e='comment-text-area']")
        page.fill("textarea[data-e2e='comment-text-area']", message)
        page.click("button[data-e2e='comment-post']")

        browser.close()

# Main execution
videos = get_fashion_videos()
for video in videos:
    fashion_items = ["Nike Shoes", "Adidas Hoodie"]  # Replace with AI detection logic
    product_links = [search_amazon_product(item) for item in fashion_items]
    
    comment_text = f"Love this look! Get similar styles here: {', '.join(product_links)} #fashion"
    comment_on_video(video, comment_text)

    time.sleep(60)  # Delay between comments
