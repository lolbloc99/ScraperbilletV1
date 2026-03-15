#!/usr/bin/env python3
"""
DEBUG SCRAPER EXECUTION - Teste l'exécution complète du scraper
Avec logging détaillé de chaque étape
"""

import json
import logging
import os
import sys
from datetime import datetime
from scraper_mongodb import ConcertScraperMongoDB

# Configuration du logging très détaillée
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    handlers=[
        logging.FileHandler('debug_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

print("\n" + "="*80)
print("🔧 DEBUG SCRAPER EXECUTION - Exécution complète avec logging")
print("="*80 + "\n")

# ============================================================================
# TEST 1: Vérifier les variables d'environnement
# ============================================================================
print("[TEST 1] Variables d'environnement...")
print("-" * 80)

mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/scraperbillet')
logger.info(f"MONGODB_URI: {mongodb_uri}")
logger.info(f"HOME: {os.getenv('HOME', 'NOT SET')}")
logger.info(f"PATH: {os.getenv('PATH', 'NOT SET')}")

# ============================================================================
# TEST 2: Charger config
# ============================================================================
print("\n[TEST 2] Chargement config...")
print("-" * 80)

try:
    with open('config.json') as f:
        config = json.load(f)
    logger.info(f"✅ Config chargée")
    logger.info(f"   Markets: {list(config['markets'].keys())}")
except Exception as e:
    logger.error(f"❌ Erreur config: {e}")
    sys.exit(1)

# ============================================================================
# TEST 3: Créer le scraper (teste MongoDB connection)
# ============================================================================
print("\n[TEST 3] Création du scraper (teste MongoDB)...")
print("-" * 80)

try:
    scraper = ConcertScraperMongoDB(mongodb_uri=mongodb_uri)
    logger.info("✅ Scraper créé avec succès")
except Exception as e:
    logger.error(f"❌ Erreur création scraper: {e}")
    logger.error(f"   Cela signifie que MongoDB n'est pas accessible")
    logger.warning(f"   On continue quand même pour tester le scraping...")
    scraper = None

# ============================================================================
# TEST 4: Tester scrape_songkick directement
# ============================================================================
print("\n[TEST 4] Test scrape_songkick (UK)...")
print("-" * 80)

if scraper:
    try:
        market = "UK"
        market_config = config['markets'][market]
        logger.info(f"Market: {market}")
        logger.info(f"Songkick URL: {market_config['songkick_url']}")

        events = scraper.scrape_songkick(market, market_config)

        logger.info(f"\n✅ Scrape Songkick retourné: {len(events)} événements")
        for i, event in enumerate(events[:5]):
            logger.info(f"   [{i+1}] {event['title']}")

        if len(events) == 0:
            logger.warning("⚠️  0 événements trouvés pour Songkick UK!")

    except Exception as e:
        logger.error(f"❌ Erreur scrape_songkick: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ============================================================================
# TEST 5: Tester scrape_viagogo directement
# ============================================================================
print("\n[TEST 5] Test scrape_viagogo (UK)...")
print("-" * 80)

if scraper:
    try:
        market = "UK"
        market_config = config['markets'][market]
        logger.info(f"Market: {market}")
        logger.info(f"Viagogo URL: {market_config['viagogo_url']}")

        events = scraper.scrape_viagogo(market, market_config)

        logger.info(f"\n✅ Scrape Viagogo retourné: {len(events)} événements")
        for i, event in enumerate(events[:5]):
            logger.info(f"   [{i+1}] {event['title']}")

        if len(events) == 0:
            logger.warning("⚠️  0 événements trouvés pour Viagogo UK!")

    except Exception as e:
        logger.error(f"❌ Erreur scrape_viagogo: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ============================================================================
# TEST 6: Exécuter l'intégralité du scraper
# ============================================================================
print("\n[TEST 6] Exécution complète scraper.execute()...")
print("-" * 80)

if scraper:
    try:
        logger.info("Démarrage du scraping complet...")
        result = scraper.execute()

        logger.info(f"\n✅ Scraping terminé!")
        logger.info(f"   Total événements trouvés: {result.get('total_events', 0)}")
        logger.info(f"   Nouveaux événements: {result.get('new_events', 0)}")

        if result.get('total_events', 0) == 0:
            logger.warning("⚠️  0 ÉVÉNEMENTS TROUVÉS AU TOTAL!")
            logger.info("\nCela signifie:")
            logger.info("  - Les URLs chargent correctement")
            logger.info("  - Mais les éléments de concerts ne sont pas trouvés")
            logger.info("  - Vérifiez que les patterns /concerts/ et /Concert-Tickets/ existent")

        scraper.close()

    except Exception as e:
        logger.error(f"❌ Erreur execution scraper: {e}")
        import traceback
        logger.error(traceback.format_exc())

# ============================================================================
# RÉSUMÉ
# ============================================================================
print("\n" + "="*80)
print("✅ DEBUG COMPLET TERMINÉ")
print("="*80)
print("\nVérifiez debug_scraper.log pour:")
print("  1. Erreurs MongoDB")
print("  2. Erreurs Selenium/Chrome")
print("  3. Nombres d'éléments trouvés vs événements extraits")
print("  4. Titres d'événements trouvés\n")
