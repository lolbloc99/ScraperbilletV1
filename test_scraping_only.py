#!/usr/bin/env python3
"""
Test just the scraping logic (no MongoDB required)
Shows the exact logging output from Selenium/Browser automation
"""

import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
from datetime import datetime

# Configure logging to show EVERYTHING
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load config
with open('config.json', 'r') as f:
    config = json.load(f)

print("\n" + "="*80)
print("🔍 SCRAPER DIAGNOSTIC - Direct Selenium Testing")
print("="*80)
print(f"This runs the scraper WITHOUT MongoDB to show exact browser behavior\n")

def test_songkick_directly():
    """Test Songkick scraping directly"""
    print("\n" + "="*80)
    print("🎵 SONGKICK UK - Testing")
    print("="*80)

    options = Options()
    if config['scrape_settings']['headless']:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        logger.warning(f"Service failed: {e}, trying without service")
        driver = webdriver.Chrome(options=options)

    try:
        market = "UK"
        market_config = config['markets'][market]
        url = f"https://www.songkick.com/metro_areas/{market_config['country_code']}"

        logger.info(f"Scraping Songkick pour {market}...")
        logger.info(f"Accès à: {url}")
        driver.get(url)

        logger.info(f"Songkick {market}: Initial page loaded, waiting 5s for JS...")
        time.sleep(5)

        # Try the selectors
        logger.info(f"Songkick {market}: Testing selectors...")

        events_elements = driver.find_elements(By.CLASS_NAME, "event-listing")
        logger.info(f"Songkick {market}: {len(events_elements)} événements trouvés avec '.event-listing'")

        if not events_elements:
            events_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-artist-name]")
            logger.info(f"Songkick {market}: {len(events_elements)} trouvés avec 'div[data-artist-name]'")

        if not events_elements:
            events_elements = driver.find_elements(By.CSS_SELECTOR, "[data-event-id]")
            logger.info(f"Songkick {market}: {len(events_elements)} trouvés avec '[data-event-id]'")

        if not events_elements:
            events_elements = driver.find_elements(By.TAG_NAME, "article")
            logger.info(f"Songkick {market}: {len(events_elements)} trouvés avec 'article'")

        # Get body text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"Songkick {market}: Body text length: {len(body_text)} chars")
        logger.info(f"Songkick {market}: Keywords - concert: {'concert' in body_text.lower()}, event: {'event' in body_text.lower()}")

        # Show first 500 chars of body text
        print(f"\n📄 First 500 chars of body text:")
        print(body_text[:500])
        print("...")

    finally:
        driver.quit()


def test_viagogo_directly():
    """Test Viagogo scraping directly"""
    print("\n" + "="*80)
    print("🎫 VIAGOGO - Testing")
    print("="*80)

    options = Options()
    if config['scrape_settings']['headless']:
        options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except Exception as e:
        logger.warning(f"Service failed: {e}, trying without service")
        driver = webdriver.Chrome(options=options)

    try:
        market = "UK"
        market_config = config['markets'][market]
        url = market_config['viagogo_url']

        logger.info(f"Scraping Viagogo pour {market}...")
        logger.info(f"Accès à: {url}")
        driver.get(url)

        logger.info(f"Viagogo {market}: Initial page loaded, waiting 5s for JS...")
        time.sleep(5)

        # Try the selectors
        logger.info(f"Viagogo {market}: Testing selectors...")

        events_elements = driver.find_elements(By.CLASS_NAME, "event-card")
        logger.info(f"Viagogo {market}: {len(events_elements)} événements trouvés avec '.event-card'")

        if not events_elements:
            events_elements = driver.find_elements(By.CSS_SELECTOR, "[data-eventid]")
            logger.info(f"Viagogo {market}: {len(events_elements)} trouvés avec '[data-eventid]'")

        if not events_elements:
            events_elements = driver.find_elements(By.CSS_SELECTOR, ".card")
            logger.info(f"Viagogo {market}: {len(events_elements)} trouvés avec '.card'")

        if not events_elements:
            events_elements = driver.find_elements(By.TAG_NAME, "article")
            logger.info(f"Viagogo {market}: {len(events_elements)} trouvés avec 'article'")

        # Get body text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        logger.info(f"Viagogo {market}: Body text length: {len(body_text)} chars")
        logger.info(f"Viagogo {market}: Keywords - concert: {'concert' in body_text.lower()}, ticket: {'ticket' in body_text.lower()}")

        # Show first 500 chars of body text
        print(f"\n📄 First 500 chars of body text:")
        print(body_text[:500])
        print("...")

    finally:
        driver.quit()


if __name__ == '__main__':
    try:
        test_songkick_directly()
        test_viagogo_directly()

        print("\n" + "="*80)
        print("✅ Diagnostic complete - check logs above for details")
        print("="*80)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
