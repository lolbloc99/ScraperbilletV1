#!/usr/bin/env python3
"""
Test CSS selectors on Songkick and Viagogo to find correct ones
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def test_songkick():
    """Test Songkick selectors"""
    print("\n" + "="*60)
    print("🎵 TESTING SONGKICK")
    print("="*60)

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
        url = "https://www.songkick.com/metro_areas/GB"
        print(f"\n📍 URL: {url}")
        driver.get(url)
        time.sleep(3)

        # Test selectors one by one
        selectors_to_test = [
            (".event-listing", "Event listing (original)"),
            (".event", "Event class"),
            ("[data-eventid]", "Data eventid attribute"),
            ("div[class*='event']", "Div with event in class"),
            (".event-card", "Event card"),
            ("article", "Article tag"),
            ("li[data-event-id]", "Li with data-event-id"),
            (".concerts-list-item", "Concerts list item"),
            ("[data-testid*='event']", "Data testid with event"),
            ("div.eventListItem", "Event list item"),
        ]

        results = {}
        for selector, description in selectors_to_test:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                count = len(elements)
                results[selector] = {
                    "description": description,
                    "count": count,
                    "status": "✓ FOUND" if count > 0 else "✗ NOT FOUND"
                }
                print(f"  {selector:40} - {description:30} - {count:3} elements")
            except Exception as e:
                print(f"  {selector:40} - ERROR: {str(e)[:30]}")

        # Also try to get all divs with 'event' in any attribute
        print(f"\n📊 Summary:")
        found_any = False
        for selector, data in results.items():
            if data['count'] > 0:
                found_any = True
                print(f"  ✓ {selector}: {data['count']} elements")

        if not found_any:
            print("  ✗ No event elements found with any selector!")
            print("\n💡 Possible reasons:")
            print("    - Website structure has changed")
            print("    - Events are dynamically loaded with JavaScript")
            print("    - Anti-bot protection is blocking the scraper")

        return results

    finally:
        driver.quit()


def test_viagogo():
    """Test Viagogo selectors"""
    print("\n" + "="*60)
    print("🎫 TESTING VIAGOGO")
    print("="*60)

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
        url = "https://www.viagogo.com/concerts"
        print(f"\n📍 URL: {url}")
        driver.get(url)
        time.sleep(3)

        selectors_to_test = [
            (".event-card", "Event card (original)"),
            (".card", "Card class"),
            ("[data-eventid]", "Data eventid attribute"),
            ("div[class*='event']", "Div with event in class"),
            (".event", "Event class"),
            (".event-item", "Event item"),
            ("article", "Article tag"),
            (".concert", "Concert class"),
            (".show-card", "Show card"),
            ("[data-testid*='event']", "Data testid with event"),
        ]

        results = {}
        for selector, description in selectors_to_test:
            try:
                elements = driver.find_elements(By.CSS_SELECTOR, selector)
                count = len(elements)
                results[selector] = {
                    "description": description,
                    "count": count,
                    "status": "✓ FOUND" if count > 0 else "✗ NOT FOUND"
                }
                print(f"  {selector:40} - {description:30} - {count:3} elements")
            except Exception as e:
                print(f"  {selector:40} - ERROR: {str(e)[:30]}")

        print(f"\n📊 Summary:")
        found_any = False
        for selector, data in results.items():
            if data['count'] > 0:
                found_any = True
                print(f"  ✓ {selector}: {data['count']} elements")

        if not found_any:
            print("  ✗ No event elements found with any selector!")
            print("\n💡 Possible reasons:")
            print("    - Website structure has changed")
            print("    - Events are dynamically loaded with JavaScript")
            print("    - Anti-bot protection is blocking the scraper")

        return results

    finally:
        driver.quit()


if __name__ == '__main__':
    print("\n🔍 SELECTOR DIAGNOSTIC TOOL")
    print("Testing which CSS selectors work on Songkick and Viagogo...")

    songkick_results = test_songkick()
    viagogo_results = test_viagogo()

    # Save results to JSON
    with open('selector_test_results.json', 'w') as f:
        json.dump({
            'songkick': songkick_results,
            'viagogo': viagogo_results,
            'timestamp': time.time()
        }, f, indent=2)

    print("\n" + "="*60)
    print("✅ Results saved to selector_test_results.json")
    print("="*60)
