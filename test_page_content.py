#!/usr/bin/env python3
"""
Diagnostic: Check what actual HTML content is being loaded
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def diagnose_songkick():
    """Diagnose what's actually loaded from Songkick"""
    print("\n" + "="*60)
    print("🎵 SONGKICK - CONTENT DIAGNOSTIC")
    print("="*60)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(options=options)

    try:
        url = "https://www.songkick.com/metro_areas/GB"
        print(f"\n📍 URL: {url}")
        driver.get(url)

        print("⏳ Waiting for page to fully load (5s)...")
        time.sleep(5)

        # Get page info
        title = driver.title
        current_url = driver.current_url
        print(f"\n📄 Page Title: {title}")
        print(f"🔗 Current URL: {current_url}")

        # Check if redirected
        if current_url != url:
            print(f"⚠️  Page redirected!")

        # Get page source snippet
        page_source = driver.page_source
        print(f"\n📊 Page source length: {len(page_source)} characters")

        # Check for error indicators
        if "error" in page_source.lower():
            print("⚠️  'error' found in page")
        if "404" in page_source:
            print("⚠️  '404' found in page")
        if "blocked" in page_source.lower():
            print("⚠️  'blocked' found in page")
        if "cloudflare" in page_source.lower():
            print("⚠️  'cloudflare' detected")
        if "captcha" in page_source.lower():
            print("⚠️  'captcha' found in page")

        # Count DOM elements
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        all_spans = driver.find_elements(By.TAG_NAME, "span")
        all_a = driver.find_elements(By.TAG_NAME, "a")

        print(f"\n🔢 DOM Elements:")
        print(f"   DIV elements: {len(all_divs)}")
        print(f"   SPAN elements: {len(all_spans)}")
        print(f"   A (link) elements: {len(all_a)}")

        # Save a sample of the HTML
        with open('/tmp/ScraperbilletV1/songkick_page_sample.html', 'w') as f:
            f.write(page_source[:5000])
        print(f"\n💾 First 5000 chars saved to songkick_page_sample.html")

        # Try scrolling to trigger lazy loading
        print("\n⏳ Scrolling page to trigger lazy loading...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Check again
        all_divs_after = driver.find_elements(By.TAG_NAME, "div")
        print(f"   DIV elements after scroll: {len(all_divs_after)} (was {len(all_divs)})")

        # Look for specific keywords
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n📝 Body text length: {len(body_text)} characters")
        print(f"   Contains 'concert': {'concert' in body_text.lower()}")
        print(f"   Contains 'event': {'event' in body_text.lower()}")
        print(f"   Contains 'artist': {'artist' in body_text.lower()}")

        if len(body_text) < 100:
            print(f"\n⚠️  Page body text is very short:")
            print(body_text[:200])

    finally:
        driver.quit()


def diagnose_viagogo():
    """Diagnose what's actually loaded from Viagogo"""
    print("\n" + "="*60)
    print("🎫 VIAGOGO - CONTENT DIAGNOSTIC")
    print("="*60)

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--start-maximized')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(options=options)

    try:
        url = "https://www.viagogo.com/concerts"
        print(f"\n📍 URL: {url}")
        driver.get(url)

        print("⏳ Waiting for page to fully load (5s)...")
        time.sleep(5)

        # Get page info
        title = driver.title
        current_url = driver.current_url
        print(f"\n📄 Page Title: {title}")
        print(f"🔗 Current URL: {current_url}")

        # Check if redirected
        if current_url != url:
            print(f"⚠️  Page redirected!")

        # Get page source snippet
        page_source = driver.page_source
        print(f"\n📊 Page source length: {len(page_source)} characters")

        # Check for error indicators
        if "error" in page_source.lower():
            print("⚠️  'error' found in page")
        if "404" in page_source:
            print("⚠️  '404' found in page")
        if "blocked" in page_source.lower():
            print("⚠️  'blocked' found in page")
        if "cloudflare" in page_source.lower():
            print("⚠️  'cloudflare' detected")
        if "captcha" in page_source.lower():
            print("⚠️  'captcha' found in page")

        # Count DOM elements
        all_divs = driver.find_elements(By.TAG_NAME, "div")
        all_spans = driver.find_elements(By.TAG_NAME, "span")
        all_a = driver.find_elements(By.TAG_NAME, "a")

        print(f"\n🔢 DOM Elements:")
        print(f"   DIV elements: {len(all_divs)}")
        print(f"   SPAN elements: {len(all_spans)}")
        print(f"   A (link) elements: {len(all_a)}")

        # Save a sample of the HTML
        with open('/tmp/ScraperbilletV1/viagogo_page_sample.html', 'w') as f:
            f.write(page_source[:5000])
        print(f"\n💾 First 5000 chars saved to viagogo_page_sample.html")

        # Try scrolling to trigger lazy loading
        print("\n⏳ Scrolling page to trigger lazy loading...")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # Check again
        all_divs_after = driver.find_elements(By.TAG_NAME, "div")
        print(f"   DIV elements after scroll: {len(all_divs_after)} (was {len(all_divs)})")

        # Look for specific keywords
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n📝 Body text length: {len(body_text)} characters")
        print(f"   Contains 'concert': {'concert' in body_text.lower()}")
        print(f"   Contains 'event': {'event' in body_text.lower()}")
        print(f"   Contains 'ticket': {'ticket' in body_text.lower()}")

        if len(body_text) < 100:
            print(f"\n⚠️  Page body text is very short:")
            print(body_text[:200])

    finally:
        driver.quit()


if __name__ == '__main__':
    print("\n🔍 PAGE CONTENT DIAGNOSTIC")
    print("Checking what's actually being loaded by Selenium...")

    diagnose_songkick()
    diagnose_viagogo()

    print("\n" + "="*60)
    print("✅ Diagnostic complete")
    print("="*60)
