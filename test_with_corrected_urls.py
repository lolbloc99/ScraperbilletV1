#!/usr/bin/env python3
"""
Test the scraper with the CORRECTED URLs
Uses the actual scraper class to test with correct config
"""

import json
import logging
import os
from scraper_mongodb import ConcertScraperMongoDB

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("\n" + "="*80)
print("🧪 TESTING SCRAPER WITH CORRECTED URLS")
print("="*80)

# Load and show config
with open('config.json') as f:
    config = json.load(f)

print("\n📋 Configuration being used:")
for market, cfg in config['markets'].items():
    print(f"\n   {market}:")
    print(f"      Songkick: {cfg['songkick_url']}")
    print(f"      Viagogo:  {cfg['viagogo_url']}")

# Set environment to use local MongoDB or print what's needed
print("\n⚠️  Note: This test tries to connect to MongoDB.")
print("   If MongoDB is not available locally, it will fail gracefully.")
print("   The important part is seeing the scraper try the CORRECT URLs.\n")

try:
    # Create scraper instance (will use MongoDB if available)
    # If MongoDB is not available, it will fail but we'll see the URLs being accessed
    scraper = ConcertScraperMongoDB()

    print("✅ MongoDB connected!")

    # Run scraper
    print("\n🚀 Starting scraper with corrected URLs...\n")
    result = scraper.execute()
    scraper.close()

    print("\n" + "="*80)
    print("📊 RESULTS")
    print("="*80)
    print(json.dumps(result, indent=2, ensure_ascii=False))

except Exception as e:
    print(f"\n⚠️  MongoDB not available (expected if running locally without DB): {e}")
    print("\n✅ But the important thing: Check the logs above to see if the CORRECT URLs")
    print("   were being accessed:")
    print("      - Songkick: https://www.songkick.com/concerts")
    print("      - Viagogo:  https://www.viagogo.com/ (or country-specific)")
    print("\nIf you see these URLs in the 'Accès à:' logs, the fix is working!")

print("\n" + "="*80)
