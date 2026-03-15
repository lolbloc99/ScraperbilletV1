#!/usr/bin/env python3
"""
Version alternative du scraper utilisant requests HTTP au lieu de Selenium
Testera si les événements peuvent être trouvés sans Selenium
"""

import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)

def scrape_songkick_http():
    """Scrape Songkick en utilisant requests HTTP"""
    logger.info("🎵 Scraping Songkick avec HTTP...")

    try:
        url = "https://www.songkick.com/concerts"
        logger.info(f"   URL: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        logger.info(f"   ✓ Page chargée: {len(response.text)} chars, status {response.status_code}")

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)

        logger.info(f"   ✓ Total <a> tags: {len(all_links)}")

        # Filter for concert links
        concert_links = []
        for link in all_links:
            href = link.get('href', '')
            if "/concerts/" in href and "-" in href.split("/concerts/")[-1]:
                concert_links.append(link)

        logger.info(f"   ✓ Liens /concerts/ trouvés: {len(concert_links)}")

        # Extract events
        events = []
        for link in concert_links:
            title = link.get_text(strip=True) if link.get_text(strip=True) else "Unknown"
            if title and len(title) > 3:
                events.append({
                    'title': title[:100],
                    'url': link.get('href')
                })

        logger.info(f"   ✓ Événements extraits: {len(events)}")

        if events:
            for event in events[:5]:
                logger.info(f"      - {event['title']}")

        return events

    except Exception as e:
        logger.error(f"   ❌ Erreur: {e}")
        return []


def scrape_viagogo_http():
    """Scrape Viagogo en utilisant requests HTTP"""
    logger.info("🎫 Scraping Viagogo avec HTTP...")

    try:
        url = "https://www.viagogo.com/"
        logger.info(f"   URL: {url}")

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        logger.info(f"   ✓ Page chargée: {len(response.text)} chars, status {response.status_code}")

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        all_links = soup.find_all('a', href=True)

        logger.info(f"   ✓ Total <a> tags: {len(all_links)}")

        # Filter for concert links
        concert_links = []
        for link in all_links:
            href = link.get('href', '')
            if "/Concert-Tickets/" in href:
                concert_links.append(link)

        logger.info(f"   ✓ Liens /Concert-Tickets/ trouvés: {len(concert_links)}")

        # Extract events
        events = []
        for link in concert_links:
            title = link.get_text(strip=True)

            # If no text, extract from URL
            if not title:
                href = link.get('href', '')
                parts = href.split("/Concert-Tickets/")
                if len(parts) > 1:
                    artist_part = parts[1].split("/")[-1]
                    title = artist_part.replace("-Tickets", "").replace("-", " ")

            if title and len(title) > 3:
                events.append({
                    'title': title[:100],
                    'url': link.get('href')
                })

        logger.info(f"   ✓ Événements extraits: {len(events)}")

        if events:
            for event in events[:5]:
                logger.info(f"      - {event['title']}")

        return events

    except Exception as e:
        logger.error(f"   ❌ Erreur: {e}")
        return []


if __name__ == '__main__':
    logger.info("\n" + "="*80)
    logger.info("🔍 TEST SCRAPER HTTP (sans Selenium)")
    logger.info("="*80 + "\n")

    songkick_events = scrape_songkick_http()
    viagogo_events = scrape_viagogo_http()

    logger.info("\n" + "="*80)
    logger.info(f"RÉSULTATS: Songkick={len(songkick_events)} | Viagogo={len(viagogo_events)}")
    logger.info("="*80)
