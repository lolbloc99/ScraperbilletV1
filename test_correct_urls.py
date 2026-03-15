#!/usr/bin/env python3
"""
Test CSS selectors on the WORKING URLs to find correct ones
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def test_songkick_concerts():
    """Test Songkick concerts page"""
    print("\n" + "="*80)
    print("🎵 SONGKICK CONCERTS (https://www.songkick.com/concerts)")
    print("="*80)

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
        url = "https://www.songkick.com/concerts"
        driver.get(url)
        time.sleep(5)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n✅ Page loaded successfully ({len(body_text)} chars)")
        print(f"   Contains 'concert': {'concert' in body_text.lower()}")
        print(f"   Contains 'event': {'event' in body_text.lower()}")

        # Try selectors
        selectors = [
            ".event",
            ".event-listing",
            ".event-card",
            "[data-id]",
            "[data-event-id]",
            "div[class*='event']",
            ".gig",
            ".concert",
            "article",
            "li",
            ".list-item",
        ]

        print(f"\n🔍 Testing CSS selectors:")
        found_working = []
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 0:
                    print(f"   ✅ {selector:30} - {len(elements):4} elements")
                    found_working.append((selector, len(elements)))
            except:
                pass

        if found_working:
            print(f"\n💡 Recommended selectors for Songkick:")
            for selector, count in found_working[:3]:
                print(f"   - {selector} ({count} elements)")
        else:
            print(f"\n⚠️  No elements found")

        # Show page structure
        divs = driver.find_elements(By.TAG_NAME, "div")
        spans = driver.find_elements(By.TAG_NAME, "span")
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"\n📊 DOM structure:")
        print(f"   DIVs: {len(divs)}, SPANs: {len(spans)}, Links: {len(links)}")

    finally:
        driver.quit()


def test_viagogo_home():
    """Test Viagogo homepage"""
    print("\n" + "="*80)
    print("🎫 VIAGOGO HOME (https://www.viagogo.com/)")
    print("="*80)

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
        url = "https://www.viagogo.com/"
        driver.get(url)
        time.sleep(5)

        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"\n✅ Page loaded successfully ({len(body_text)} chars)")
        print(f"   Contains 'concert': {'concert' in body_text.lower()}")
        print(f"   Contains 'ticket': {'ticket' in body_text.lower()}")
        print(f"   Contains 'event': {'event' in body_text.lower()}")

        # Try selectors
        selectors = [
            ".event",
            ".event-card",
            "[data-id]",
            "[data-event-id]",
            "div[class*='event']",
            ".card",
            ".concert",
            "article",
            "li",
            ".listing",
            "[data-testid*='event']",
            "div[class*='card']",
        ]

        print(f"\n🔍 Testing CSS selectors:")
        found_working = []
        for selector in selectors:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                if len(elements) > 0:
                    print(f"   ✅ {selector:30} - {len(elements):4} elements")
                    found_working.append((selector, len(elements)))
            except:
                pass

        if found_working:
            print(f"\n💡 Recommended selectors for Viagogo:")
            for selector, count in found_working[:3]:
                print(f"   - {selector} ({count} elements)")
        else:
            print(f"\n⚠️  No elements found")

        # Show page structure
        divs = driver.find_elements(By.TAG_NAME, "div")
        spans = driver.find_elements(By.TAG_NAME, "span")
        links = driver.find_elements(By.TAG_NAME, "a")
        print(f"\n📊 DOM structure:")
        print(f"   DIVs: {len(divs)}, SPANs: {len(spans)}, Links: {len(links)}")

    finally:
        driver.quit()


if __name__ == '__main__':
    print("\n🔍 FINDING WORKING SELECTORS FOR CORRECTED URLS")
    print("Testing the working homepage URLs to find correct CSS selectors...\n")

    test_songkick_concerts()
    test_viagogo_home()

    print("\n" + "="*80)
    print("✅ Selector testing complete")
    print("="*80)
