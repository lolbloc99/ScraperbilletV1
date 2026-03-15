import json
import logging
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
import time
from datetime import datetime, timedelta
from typing import List, Dict
import hashlib
import os
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import certifi

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

class MongoDBManager:
    """Gestionnaire MongoDB"""
    def __init__(self, mongodb_uri: str, db_name: str = "scraperbillet"):
        """Initialiser la connexion MongoDB"""
        try:
            self.client = MongoClient(
                mongodb_uri,
                serverSelectionTimeoutMS=5000,
                tlsCAFile=certifi.where() if "mongodb+srv" in mongodb_uri else None
            )
            # Tester la connexion
            self.client.admin.command('ping')
            self.db = self.client[db_name]
            self.events_collection = self.db['events']
            self.metadata_collection = self.db['metadata']
            logger.info("✓ Connecté à MongoDB")
        except ConnectionFailure as e:
            logger.error(f"❌ Erreur connexion MongoDB: {e}")
            raise

    def save_event(self, event: Dict) -> bool:
        """Sauvegarder un événement"""
        try:
            event_hash = self._generate_event_hash(event)

            # Vérifier si l'événement existe déjà
            if self.events_collection.find_one({"_id": event_hash}):
                return False  # Déjà existant

            event['_id'] = event_hash
            event['created_at'] = datetime.now()
            self.events_collection.insert_one(event)
            return True
        except Exception as e:
            logger.error(f"Erreur sauvegarde événement: {e}")
            return False

    def get_new_events(self, hours: int = 24) -> List[Dict]:
        """Récupérer les nouveaux événements"""
        try:
            since = datetime.now() - timedelta(hours=hours)
            events = list(self.events_collection.find({
                "created_at": {"$gte": since}
            }).sort("created_at", -1))

            # Retirer le field _id pour la sérialisation
            for event in events:
                event.pop('_id', None)

            return events
        except Exception as e:
            logger.error(f"Erreur récupération événements: {e}")
            return []

    def get_all_events(self) -> List[Dict]:
        """Récupérer tous les événements"""
        try:
            events = list(self.events_collection.find().sort("created_at", -1))
            for event in events:
                event.pop('_id', None)
            return events
        except Exception as e:
            logger.error(f"Erreur récupération tous les événements: {e}")
            return []

    def get_statistics(self) -> Dict:
        """Obtenir les statistiques"""
        try:
            total_events = self.events_collection.count_documents({})
            sold_out_count = self.events_collection.count_documents({"sold_out": True})

            by_market = {}
            for doc in self.events_collection.aggregate([
                {"$group": {"_id": "$market", "count": {"$sum": 1}}}
            ]):
                by_market[doc['_id']] = doc['count']

            return {
                "total_events": total_events,
                "sold_out": sold_out_count,
                "by_market": by_market,
                "last_update": self.get_last_update()
            }
        except Exception as e:
            logger.error(f"Erreur statistiques: {e}")
            return {}

    def get_last_update(self) -> str:
        """Obtenir la date du dernier update"""
        try:
            meta = self.metadata_collection.find_one({"_id": "last_update"})
            if meta:
                return meta.get("timestamp", "Unknown")
            return "Never"
        except:
            return "Unknown"

    def save_metadata(self, metadata: Dict):
        """Sauvegarder les métadonnées"""
        try:
            metadata['_id'] = "last_update"
            self.metadata_collection.replace_one(
                {"_id": "last_update"},
                metadata,
                upsert=True
            )
        except Exception as e:
            logger.error(f"Erreur sauvegarde metadata: {e}")

    def _generate_event_hash(self, event: Dict) -> str:
        """Générer un hash unique pour un événement"""
        key = f"{event['title']}{event['date']}{event['market']}{event['url']}"
        return hashlib.md5(key.encode()).hexdigest()

    def close(self):
        """Fermer la connexion"""
        try:
            self.client.close()
            logger.info("Connexion MongoDB fermée")
        except:
            pass


class ConcertScraperMongoDB:
    def __init__(self, config_file='config.json', mongodb_uri: str = None):
        """Initialiser le scraper avec MongoDB"""
        with open(config_file, 'r', encoding='utf-8') as f:
            self.config = json.load(f)

        # Utiliser la variable d'environnement ou le paramètre
        if mongodb_uri is None:
            mongodb_uri = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/scraperbillet')

        self.db = MongoDBManager(mongodb_uri)
        self.new_events = []

    def scrape_songkick(self, market: str, market_config: Dict) -> List[Dict]:
        """Scraper Songkick pour un marché donné"""
        logger.info(f"Scraping Songkick pour {market}...")
        events = []

        try:
            options = Options()
            if self.config['scrape_settings']['headless']:
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument('--disable-dev-shm-usage')
                options.add_argument('--disable-gpu')

            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            # Configuration ChromeDriver - webdriver-manager détecte la version
            try:
                service = Service(ChromeDriverManager().install())
            except Exception as e:
                logger.warning(f"WebDriver manager failed, trying without service: {e}")
                service = None

            if service:
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)

            url = f"https://www.songkick.com/metro_areas/{market_config['country_code']}"
            logger.info(f"Accès à: {url}")
            driver.get(url)

            # Attendre que la page se charge complètement (JavaScript)
            time.sleep(5)
            logger.info(f"Songkick {market}: Page chargée, recherche des éléments...")

            # Essayer plusieurs sélecteurs
            events_elements = driver.find_elements(By.CLASS_NAME, "event-listing")
            if not events_elements:
                logger.info(f"Songkick {market}: .event-listing not found, trying alternatives...")
                # Essayer d'autres sélecteurs
                events_elements = driver.find_elements(By.CSS_SELECTOR, "div[data-artist-name]")
            if not events_elements:
                events_elements = driver.find_elements(By.CSS_SELECTOR, "[data-event-id]")
            if not events_elements:
                events_elements = driver.find_elements(By.TAG_NAME, "article")

            # Dernière tentative - regarder le contenu de la page
            body_text = driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"Songkick {market}: Body text length: {len(body_text)}, Keywords found - concert: {'concert' in body_text.lower()}, event: {'event' in body_text.lower()}")

            logger.info(f"Songkick {market}: {len(events_elements)} événements trouvés avec sélecteurs testés")

            for event_elem in events_elements:
                try:
                    title = event_elem.find_element(By.CLASS_NAME, "event-title").text
                    date_elem = event_elem.find_element(By.CLASS_NAME, "event-date")
                    date = date_elem.text if date_elem else "Date unknown"
                    is_sold_out = "sold out" in event_elem.text.lower()

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

                    # Garder TOUS les événements, pas seulement sold out
                    events.append(event)
                    if is_sold_out:
                        logger.info(f"✓ {market} Songkick: {title} - SOLD OUT")
                    else:
                        logger.info(f"✓ {market} Songkick: {title} - Disponible")

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
                options.add_argument('--disable-gpu')

            options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

            # Configuration ChromeDriver - webdriver-manager détecte la version
            try:
                service = Service(ChromeDriverManager().install())
            except Exception as e:
                logger.warning(f"WebDriver manager failed, trying without service: {e}")
                service = None

            if service:
                driver = webdriver.Chrome(service=service, options=options)
            else:
                driver = webdriver.Chrome(options=options)

            url = market_config['viagogo_url']
            logger.info(f"Accès à: {url}")
            driver.get(url)

            # Attendre que la page se charge complètement (JavaScript)
            time.sleep(5)
            logger.info(f"Viagogo {market}: Page chargée, recherche des éléments...")

            # Essayer plusieurs sélecteurs
            events_elements = driver.find_elements(By.CLASS_NAME, "event-card")
            if not events_elements:
                logger.info(f"Viagogo {market}: .event-card not found, trying alternatives...")
                events_elements = driver.find_elements(By.CSS_SELECTOR, "[data-eventid]")
            if not events_elements:
                events_elements = driver.find_elements(By.CSS_SELECTOR, ".card")
            if not events_elements:
                events_elements = driver.find_elements(By.TAG_NAME, "article")

            # Dernière tentative - regarder le contenu de la page
            body_text = driver.find_element(By.TAG_NAME, "body").text
            logger.info(f"Viagogo {market}: Body text length: {len(body_text)}, Keywords found - concert: {'concert' in body_text.lower()}, ticket: {'ticket' in body_text.lower()}")

            logger.info(f"Viagogo {market}: {len(events_elements)} événements trouvés avec sélecteurs testés")

            for event_elem in events_elements:
                try:
                    title = event_elem.find_element(By.CLASS_NAME, "event-name").text
                    date_elem = event_elem.find_element(By.CLASS_NAME, "event-date")
                    date = date_elem.text if date_elem else "Date unknown"

                    is_sold_out = "sold out" in event_elem.text.lower() or \
                                 "ausverkauft" in event_elem.text.lower() or \
                                 "épuisé" in event_elem.text.lower()

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

            songkick_events = self.scrape_songkick(market, market_config)
            all_events.extend(songkick_events)
            time.sleep(self.config['scrape_settings']['delay_between_requests'])

            viagogo_events = self.scrape_viagogo(market, market_config)
            all_events.extend(viagogo_events)
            time.sleep(self.config['scrape_settings']['delay_between_requests'])

        return all_events

    def save_new_events(self, events: List[Dict]) -> List[Dict]:
        """Sauvegarder les nouveaux événements"""
        new_events = []

        for event in events:
            if self.db.save_event(event):
                new_events.append(event)
                logger.info(f"✨ NOUVEAU: {event['market']} - {event['title']}")
            else:
                logger.debug(f"Déjà enregistré: {event['title']}")

        return new_events

    def execute(self) -> Dict:
        """Exécuter le scraping complet"""
        try:
            all_events = self.run_scrape_all_markets()
            self.new_events = self.save_new_events(all_events)

            # Sauvegarder les métadonnées
            self.db.save_metadata({
                "timestamp": datetime.now().isoformat(),
                "total_scraped": len(all_events),
                "new_events": len(self.new_events)
            })

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

    def close(self):
        """Fermer les connexions"""
        self.db.close()


def main():
    """Fonction principale"""
    scraper = ConcertScraperMongoDB('config.json')
    result = scraper.execute()
    scraper.close()

    print("\n" + "=" * 60)
    print("RÉSULTATS DU SCRAPING")
    print("=" * 60)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    return result


if __name__ == "__main__":
    main()
