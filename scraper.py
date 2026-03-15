import json
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime, timedelta
from typing import List, Dict
import hashlib
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ConcertScraper:
    def __init__(self, config_file='config.json'):
        """Initialiser le scraper avec la configuration"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        self.events_db_file = self.config['database_file']
        self.events_db = self.load_events_db()
        self.new_events = []

    def load_events_db(self) -> Dict:
        """Charger la base de données des événements"""
        if os.path.exists(self.events_db_file):
            try:
                with open(self.events_db_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                logger.warning("Impossible de charger la DB existante, création nouvelle")
                return {"events": {}, "last_updated": None}
        return {"events": {}, "last_updated": None}

    def save_events_db(self):
        """Sauvegarder la base de données"""
        self.events_db['last_updated'] = datetime.now().isoformat()
        with open(self.events_db_file, 'w', encoding='utf-8') as f:
            json.dump(self.events_db, f, ensure_ascii=False, indent=2)
        logger.info(f"DB sauvegardée avec {len(self.events_db['events'])} événements")

    def generate_event_hash(self, event: Dict) -> str:
        """Générer un hash unique pour un événement"""
        key = f"{event['title']}{event['date']}{event['market']}{event['url']}"
        return hashlib.md5(key.encode()).hexdigest()

    def scrape_songkick(self, market: str, market_config: Dict) -> List[Dict]:
        """Scraper Songkick pour un marché donné"""
        logger.info(f"Scraping Songkick pour {market}...")
        events = []

        try:
            # Utiliser Selenium pour charger le JavaScript
            options = Options()
            if self.config['scrape_settings']['headless']:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)

            # URL spécifique par pays
            url = f"https://www.songkick.com/metro_areas/{market_config['country_code']}"
            driver.get(url)

            # Attendre le chargement des événements
            time.sleep(self.config['scrape_settings']['delay_between_requests'])

            # Extraire les événements
            events_elements = driver.find_elements(By.CLASS_NAME, "event-listing")

            for event_elem in events_elements:
                try:
                    title = event_elem.find_element(By.CLASS_NAME, "event-title").text
                    date_elem = event_elem.find_element(By.CLASS_NAME, "event-date")
                    date = date_elem.text if date_elem else "Date unknown"

                    # Vérifier si sold out
                    is_sold_out = "sold out" in event_elem.text.lower()

                    # Obtenir le lien
                    link_elem = event_elem.find_element(By.TAG_NAME, "a")
                    url = link_elem.get_attribute("href") if link_elem else ""

                    event = {
                        "title": title,
                        "date": date,
                        "market": market,
                        "platform": "Songkick",
                        "url": url,
                        "sold_out": is_sold_out,
                        "scraped_at": datetime.now().isoformat()
                    }

                    if is_sold_out:
                        events.append(event)
                        logger.info(f"✓ {market} Songkick: {title} - SOLD OUT")

                except Exception as e:
                    logger.debug(f"Erreur parsing événement Songkick: {e}")
                    continue

            driver.quit()

        except Exception as e:
            logger.error(f"Erreur scraping Songkick {market}: {e}")

        return events

    def scrape_viagogo(self, market: str, market_config: Dict) -> List[Dict]:
        """Scraper Viagogo pour un marché donné"""
        logger.info(f"Scraping Viagogo pour {market}...")
        events = []

        try:
            options = Options()
            if self.config['scrape_settings']['headless']:
                options.add_argument('--headless')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(options=options)

            # URL Viagogo
            url = market_config['viagogo_url']
            driver.get(url)

            time.sleep(self.config['scrape_settings']['delay_between_requests'])

            # Extraire les événements
            events_elements = driver.find_elements(By.CLASS_NAME, "event-card")

            for event_elem in events_elements:
                try:
                    title = event_elem.find_element(By.CLASS_NAME, "event-name").text
                    date_elem = event_elem.find_element(By.CLASS_NAME, "event-date")
                    date = date_elem.text if date_elem else "Date unknown"

                    # Vérifier si sold out
                    is_sold_out = "sold out" in event_elem.text.lower() or \
                                 "ausverkauft" in event_elem.text.lower() or \
                                 "épuisé" in event_elem.text.lower()

                    # Obtenir le lien
                    link_elem = event_elem.find_element(By.TAG_NAME, "a")
                    url = link_elem.get_attribute("href") if link_elem else ""

                    event = {
                        "title": title,
                        "date": date,
                        "market": market,
                        "platform": "Viagogo",
                        "url": url,
                        "sold_out": is_sold_out,
                        "scraped_at": datetime.now().isoformat()
                    }

                    if is_sold_out:
                        events.append(event)
                        logger.info(f"✓ {market} Viagogo: {title} - SOLD OUT")

                except Exception as e:
                    logger.debug(f"Erreur parsing événement Viagogo: {e}")
                    continue

            driver.quit()

        except Exception as e:
            logger.error(f"Erreur scraping Viagogo {market}: {e}")

        return events

    def run_scrape_all_markets(self) -> List[Dict]:
        """Scraper tous les marchés"""
        all_events = []

        logger.info("=" * 60)
        logger.info(f"DÉMARRAGE DU SCRAPING - {datetime.now()}")
        logger.info("=" * 60)

        for market, market_config in self.config['markets'].items():
            logger.info(f"\n📍 Marché: {market}")

            # Scraper Songkick
            songkick_events = self.scrape_songkick(market, market_config)
            all_events.extend(songkick_events)

            # Petit délai entre les deux platforms
            time.sleep(self.config['scrape_settings']['delay_between_requests'])

            # Scraper Viagogo
            viagogo_events = self.scrape_viagogo(market, market_config)
            all_events.extend(viagogo_events)

            # Délai entre les marchés
            time.sleep(self.config['scrape_settings']['delay_between_requests'])

        return all_events

    def filter_new_events(self, events: List[Dict]) -> List[Dict]:
        """Filtrer les nouveaux événements (pas encore dans la DB)"""
        new_events = []

        for event in events:
            event_hash = self.generate_event_hash(event)

            if event_hash not in self.events_db['events']:
                new_events.append(event)
                self.events_db['events'][event_hash] = event
                logger.info(f"✨ NOUVEAU: {event['market']} - {event['title']}")
            else:
                logger.debug(f"Déjà enregistré: {event['title']}")

        return new_events

    def execute(self) -> Dict:
        """Exécuter le scraping complet"""
        try:
            # Scraper tous les marchés
            all_events = self.run_scrape_all_markets()

            # Filtrer les nouveaux événements
            self.new_events = self.filter_new_events(all_events)

            # Sauvegarder la DB
            self.save_events_db()

            logger.info("\n" + "=" * 60)
            logger.info(f"RÉSUMÉ:")
            logger.info(f"  Total événements scraped: {len(all_events)}")
            logger.info(f"  Nouveaux événements: {len(self.new_events)}")
            logger.info("=" * 60)

            return {
                "success": True,
                "total_events": len(all_events),
                "new_events": len(self.new_events),
                "events": self.new_events,
                "timestamp": datetime.now().isoformat()
            }

        except Exception as e:
            logger.error(f"Erreur fatale lors du scraping: {e}")
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }


def main():
    """Fonction principale"""
    scraper = ConcertScraper('config.json')
    result = scraper.execute()

    print("\n" + "=" * 60)
    print("RÉSULTATS DU SCRAPING")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result


if __name__ == "__main__":
    main()
