#!/usr/bin/env python3
"""
Simple test to verify the CORRECT URLs are being used
"""

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Load config
with open('config.json') as f:
    config = json.load(f)

print("\n" + "="*80)
print("🧪 TESTING CORRECTED URLS FROM CONFIG")
print("="*80)

def test_market(market_name):
    """Test scraping for a specific market"""
    print(f"\n📍 Testing market: {market_name}")
    market_config = config['markets'][market_name]

    songkick_url = market_config['songkick_url']
    viagogo_url = market_config['viagogo_url']

    print(f"   Songkick URL: {songkick_url}")
    print(f"   Viagogo URL:  {viagogo_url}")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(options=options)

    try:
        # Test Songkick
        print(f"\n   🎵 Songkick {market_name}...")
        driver.get(songkick_url)
        time.sleep(4)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        title = driver.title

        # Check for 404
        is_404 = "404" in body_text or "not found" in body_text.lower()

        # Try selectors
        event_elements = driver.find_elements(By.CLASS_NAME, "event")
        if not event_elements:
            event_elements = driver.find_elements(By.TAG_NAME, "li")

        print(f"      Title: {title[:50]}")
        print(f"      Body: {len(body_text)} chars")
        print(f"      Status: {'❌ 404 ERROR' if is_404 else '✅ OK'}")
        print(f"      Events found (.event or li): {len(event_elements)}")

        # Test Viagogo
        print(f"\n   🎫 Viagogo {market_name}...")
        driver.get(viagogo_url)
        time.sleep(4)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        title = driver.title

        is_404 = "404" in body_text or "not found" in body_text.lower()

        # Try selector
        event_elements = driver.find_elements(By.TAG_NAME, "li")

        print(f"      Title: {title[:50]}")
        print(f"      Body: {len(body_text)} chars")
        print(f"      Status: {'❌ 404 ERROR' if is_404 else '✅ OK'}")
        print(f"      Events found (li): {len(event_elements)}")

    finally:
        driver.quit()

# Test a few markets
print("\nTesting configured URLs...\n")

for market in ["UK", "France"]:
    try:
        test_market(market)
    except Exception as e:
        print(f"❌ Error testing {market}: {e}")

print("\n" + "="*80)
print("✅ URL test complete")
print("="*80 + "\n")
