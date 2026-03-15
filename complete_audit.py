#!/usr/bin/env python3
"""
COMPLETE AUDIT SCRIPT - Diagnostic complet du scraper
Teste chaque étape pour identifier le problème
"""

import json
import logging
import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import subprocess

# Configuration du logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

print("\n" + "="*80)
print("🔍 AUDIT COMPLET DU SCRAPER - Diagnostic des causes du 0 événements")
print("="*80 + "\n")

# ============================================================================
# TEST 1: Vérifier Chrome/Chromium est disponible
# ============================================================================
print("\n[TEST 1] Vérification de Chrome/Chromium disponible...")
print("-" * 80)

try:
    # Chercher Chrome/Chromium
    chrome_paths = [
        "/usr/bin/chromium-browser",
        "/usr/bin/chromium",
        "/snap/bin/chromium",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/usr/bin/google-chrome",
        "/usr/bin/google-chrome-stable",
    ]

    chrome_found = None
    for path in chrome_paths:
        if os.path.exists(path):
            chrome_found = path
            logger.info(f"✅ Chrome trouvé à: {chrome_found}")
            break

    if not chrome_found:
        logger.warning("⚠️  Chrome/Chromium non trouvé via recherche de chemins")
        logger.info("   Tentative avec webdriver-manager...")
        try:
            driver_path = ChromeDriverManager().install()
            logger.info(f"✅ WebDriver manager a installé: {driver_path}")
        except Exception as e:
            logger.error(f"❌ Erreur WebDriver manager: {e}")
    else:
        logger.info("✅ Chrome/Chromium disponible")

except Exception as e:
    logger.error(f"❌ Erreur vérification Chrome: {e}")

# ============================================================================
# TEST 2: Charger et vérifier la configuration
# ============================================================================
print("\n[TEST 2] Chargement et vérification de la configuration...")
print("-" * 80)

try:
    with open('config.json') as f:
        config = json.load(f)

    logger.info(f"✅ Config.json chargée")
    logger.info(f"   Markets configurés: {list(config['markets'].keys())}")

    for market, market_config in config['markets'].items():
        songkick_url = market_config.get('songkick_url', 'MISSING')
        viagogo_url = market_config.get('viagogo_url', 'MISSING')
        logger.info(f"\n   {market}:")
        logger.info(f"      Songkick: {songkick_url}")
        logger.info(f"      Viagogo:  {viagogo_url}")

except Exception as e:
    logger.error(f"❌ Erreur loading config: {e}")
    sys.exit(1)

# ============================================================================
# TEST 3: Test Selenium - Créer driver et charger une page
# ============================================================================
print("\n[TEST 3] Test Selenium - Création du driver...")
print("-" * 80)

driver = None
try:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
        logger.info("✅ WebDriver créé avec service")
    except Exception as e:
        logger.warning(f"⚠️  Service failed: {e}")
        driver = webdriver.Chrome(options=options)
        logger.info("✅ WebDriver créé sans service")

except Exception as e:
    logger.error(f"❌ Erreur création WebDriver: {e}")
    sys.exit(1)

# ============================================================================
# TEST 4: Tester URLs Songkick
# ============================================================================
print("\n[TEST 4] Test URLs Songkick...")
print("-" * 80)

def test_songkick_url(driver, url, market):
    """Test une URL Songkick spécifique"""
    try:
        logger.info(f"\n   📍 URL: {url}")
        logger.info(f"   Chargement...")

        driver.get(url)
        time.sleep(6)  # Attendre JS rendering

        # Vérifier que la page s'est chargée
        body_text = driver.find_element(By.TAG_NAME, "body").text
        html_size = len(driver.page_source)

        logger.info(f"   ✅ Page chargée: {html_size} chars, {len(body_text)} chars de texte")

        # Vérifier keywords
        has_concert = "concert" in body_text.lower()
        logger.info(f"   Keyword 'concert': {'✅ Oui' if has_concert else '❌ Non'}")

        # Chercher les LIENS avec pattern /concerts/
        all_links = driver.find_elements(By.TAG_NAME, "a")
        logger.info(f"   Total liens <a>: {len(all_links)}")

        concert_links = []
        for i, link in enumerate(all_links):
            href = link.get_attribute("href") or ""
            if "/concerts/" in href and "-" in href.split("/concerts/")[-1]:
                concert_links.append((i, link.text.strip()[:50] if link.text else "", href[:100]))

        logger.info(f"   🎵 Liens /concerts/ avec pattern: {len(concert_links)}")

        if concert_links:
            logger.info(f"   Exemples:")
            for idx, (link_idx, text, url) in enumerate(concert_links[:5]):
                logger.info(f"      [{link_idx}] Text: '{text}' URL: {url}...")
        else:
            logger.warning(f"   ⚠️  Aucun lien /concerts/ trouvé!")

            # DEBUG: Montrer tous les liens pour comprendre
            logger.info(f"\n   DEBUG - Premiers 10 liens trouvés:")
            for i, link in enumerate(all_links[:10]):
                href = link.get_attribute("href") or ""
                text = link.text.strip()[:30] if link.text else ""
                logger.info(f"      [{i}] {text} -> {href[:80]}")

        return len(concert_links) > 0

    except Exception as e:
        logger.error(f"   ❌ Erreur: {e}")
        return False

# Tester Songkick pour 2 markets
for market in ["UK", "France"]:
    market_config = config['markets'][market]
    url = market_config['songkick_url']
    test_songkick_url(driver, url, market)

# ============================================================================
# TEST 5: Tester URLs Viagogo
# ============================================================================
print("\n[TEST 5] Test URLs Viagogo...")
print("-" * 80)

def test_viagogo_url(driver, url, market):
    """Test une URL Viagogo spécifique"""
    try:
        logger.info(f"\n   📍 URL: {url}")
        logger.info(f"   Chargement...")

        driver.get(url)
        time.sleep(6)  # Attendre JS rendering

        # Vérifier que la page s'est chargée
        body_text = driver.find_element(By.TAG_NAME, "body").text
        html_size = len(driver.page_source)

        logger.info(f"   ✅ Page chargée: {html_size} chars, {len(body_text)} chars de texte")

        # Vérifier keywords
        has_concert = "concert" in body_text.lower()
        has_ticket = "ticket" in body_text.lower()
        logger.info(f"   Keyword 'concert': {'✅ Oui' if has_concert else '❌ Non'}")
        logger.info(f"   Keyword 'ticket': {'✅ Oui' if has_ticket else '❌ Non'}")

        # Chercher les LIENS avec pattern /Concert-Tickets/
        all_links = driver.find_elements(By.TAG_NAME, "a")
        logger.info(f"   Total liens <a>: {len(all_links)}")

        concert_links = []
        for i, link in enumerate(all_links):
            href = link.get_attribute("href") or ""
            if "/Concert-Tickets/" in href:
                text = link.text.strip()[:50] if link.text else ""
                concert_links.append((i, text, href[:100]))

        logger.info(f"   🎫 Liens /Concert-Tickets/: {len(concert_links)}")

        if concert_links:
            logger.info(f"   Exemples:")
            for idx, (link_idx, text, url) in enumerate(concert_links[:5]):
                logger.info(f"      [{link_idx}] Text: '{text}' URL: {url}...")
        else:
            logger.warning(f"   ⚠️  Aucun lien /Concert-Tickets/ trouvé!")

            # DEBUG: Montrer tous les liens
            logger.info(f"\n   DEBUG - Premiers 10 liens trouvés:")
            for i, link in enumerate(all_links[:10]):
                href = link.get_attribute("href") or ""
                text = link.text.strip()[:30] if link.text else ""
                logger.info(f"      [{i}] {text} -> {href[:80]}")

        return len(concert_links) > 0

    except Exception as e:
        logger.error(f"   ❌ Erreur: {e}")
        return False

# Tester Viagogo pour 2 markets
for market in ["UK", "France"]:
    market_config = config['markets'][market]
    url = market_config['viagogo_url']
    test_viagogo_url(driver, url, market)

# ============================================================================
# TEST 6: Simulation du scraper réel
# ============================================================================
print("\n[TEST 6] Simulation du scraper réel...")
print("-" * 80)

def simulate_scrape_market(driver, market):
    """Simule le scraping d'un marché"""
    logger.info(f"\n📍 Market: {market}")

    market_config = config['markets'][market]

    # Songkick
    logger.info(f"   🎵 Songkick:")
    url = market_config['songkick_url']
    try:
        driver.get(url)
        time.sleep(6)

        all_links = driver.find_elements(By.TAG_NAME, "a")
        events_elements = []

        for link in all_links:
            href = link.get_attribute("href") or ""
            if "/concerts/" in href and "-" in href.split("/concerts/")[-1]:
                events_elements.append(link)

        logger.info(f"      Liens trouvés: {len(events_elements)}")

        parsed = 0
        for link_elem in events_elements:
            try:
                title = link_elem.text.strip() if link_elem.text else "Unknown"
                url = link_elem.get_attribute("href") or ""

                if title and title != "Unknown" and len(title) > 3:
                    parsed += 1
                    logger.info(f"      ✓ {title[:60]}")
            except:
                pass

        logger.info(f"      Événements valides: {parsed}")

    except Exception as e:
        logger.error(f"      ❌ Erreur: {e}")

    # Viagogo
    logger.info(f"   🎫 Viagogo:")
    url = market_config['viagogo_url']
    try:
        driver.get(url)
        time.sleep(6)

        all_links = driver.find_elements(By.TAG_NAME, "a")
        events_elements = []

        for link in all_links:
            href = link.get_attribute("href") or ""
            if "/Concert-Tickets/" in href:
                events_elements.append(link)

        logger.info(f"      Liens trouvés: {len(events_elements)}")

        parsed = 0
        for link_elem in events_elements:
            try:
                title = link_elem.text.strip() if link_elem.text else ""
                url = link_elem.get_attribute("href") or ""

                if not title:
                    parts = url.split("/Concert-Tickets/")
                    if len(parts) > 1:
                        artist_part = parts[1].split("/")[-1]
                        title = artist_part.replace("-Tickets", "").replace("-", " ")

                if title and title != "Unknown" and len(title) > 3:
                    parsed += 1
                    logger.info(f"      ✓ {title[:60]}")
            except:
                pass

        logger.info(f"      Événements valides: {parsed}")

    except Exception as e:
        logger.error(f"      ❌ Erreur: {e}")

simulate_scrape_market(driver, "UK")
simulate_scrape_market(driver, "France")

# ============================================================================
# Cleanup
# ============================================================================
print("\n[Cleanup] Fermeture du driver...")
print("-" * 80)

if driver:
    driver.quit()
    logger.info("✅ Driver fermé")

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "="*80)
print("✅ AUDIT COMPLET TERMINÉ")
print("="*80)
print("\nVérifiez les logs au-dessus pour identifier:")
print("  1. Si Chrome/Chromium est disponible")
print("  2. Si les URLs se chargent correctement")
print("  3. Si les liens de concerts sont trouvés")
print("  4. Pourquoi 0 événements sont trouvés\n")
