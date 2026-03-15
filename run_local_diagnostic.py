#!/usr/bin/env python3
"""
Run the scraper locally with FULL logging output visible
This shows exactly what's happening with event detection
"""

import json
import logging
from scraper_mongodb import ConcertScraperMongoDB

# Configure logging to show EVERYTHING
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

print("\n" + "="*70)
print("🔍 LOCAL SCRAPER DIAGNOSTIC - Full Logging Output")
print("="*70 + "\n")

# Load config to show what we're scraping
with open('config.json', 'r') as f:
    config = json.load(f)

print("📋 Configuration:")
print(f"  Markets: {', '.join(config['markets'].keys())}")
print(f"  Headless: {config['scrape_settings']['headless']}")
print(f"  Timeout: {config['scrape_settings']['timeout']}s")
print(f"  Delay: {config['scrape_settings']['delay_between_requests']}s")
print()

# Run the scraper with full logging
try:
    print("🚀 Starting scraper (note: using local MongoDB)...\n")
    scraper = ConcertScraperMongoDB()
    result = scraper.execute()
    scraper.close()

    print("\n" + "="*70)
    print("📊 RESULTS")
    print("="*70)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("="*70)

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
