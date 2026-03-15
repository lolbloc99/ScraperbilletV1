#!/usr/bin/env python3
"""
Test different URL patterns to find which ones actually work
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_url(url, description):
    """Test if a URL loads without 404"""
    print(f"\n📍 Testing: {description}")
    print(f"   URL: {url}")

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
        driver.get(url)
        time.sleep(3)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        title = driver.title

        # Check for error indicators
        is_404 = "404" in body_text or "not found" in body_text.lower() or "couldn't find" in body_text.lower()
        has_content = len(body_text) > 500

        status = "❌ 404 ERROR" if is_404 else ("✅ WORKS" if has_content else "⚠️ LIMITED")

        print(f"   Status: {status}")
        print(f"   Title: {title}")
        print(f"   Body length: {len(body_text)} chars")
        print(f"   First 200 chars: {body_text[:200]}...")

        return not is_404

    finally:
        driver.quit()


print("\n" + "="*80)
print("🔍 FINDING CORRECT SONGKICK URLS")
print("="*80)

songkick_urls = [
    ("https://www.songkick.com/metro_areas/GB", "Original URL (GB)"),
    ("https://www.songkick.com/", "Songkick home"),
    ("https://www.songkick.com/concerts", "Songkick concerts"),
    ("https://www.songkick.com/metro-areas", "Metro areas (plural)"),
    ("https://www.songkick.com/find-concerts", "Find concerts"),
    ("https://www.songkick.com/concerts/search", "Concerts search"),
]

working_songkick = []
for url, desc in songkick_urls:
    if test_url(url, desc):
        working_songkick.append(url)

print("\n" + "="*80)
print("🔍 FINDING CORRECT VIAGOGO URLS")
print("="*80)

viagogo_urls = [
    ("https://www.viagogo.com/concerts", "Original URL"),
    ("https://www.viagogo.com/", "Viagogo home"),
    ("https://www.viagogo.com/concerts/search", "Concerts search"),
    ("https://www.viagogo.com/tickets/concerts", "Tickets concerts"),
    ("https://www.viagogo.fr/", "Viagogo France home"),
    ("https://www.viagogo.fr/concerts", "Viagogo France concerts"),
]

working_viagogo = []
for url, desc in viagogo_urls:
    if test_url(url, desc):
        working_viagogo.append(url)

print("\n" + "="*80)
print("📊 SUMMARY - Working URLs")
print("="*80)

if working_songkick:
    print(f"\n✅ Songkick working URLs:")
    for url in working_songkick:
        print(f"   {url}")
else:
    print(f"\n❌ No working Songkick URLs found")

if working_viagogo:
    print(f"\n✅ Viagogo working URLs:")
    for url in working_viagogo:
        print(f"   {url}")
else:
    print(f"\n❌ No working Viagogo URLs found")

print("\n" + "="*80)
