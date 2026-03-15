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
        """Scraper Songkick pour un marché donné - utilise requests HTTP"""
        logger.info(f"Scraping Songkick pour {market}...")
        events = []

        try:
            from bs4 import BeautifulSoup

            url = market_config['songkick_url']
            logger.info(f"Accès à: {url}")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate',
                'Connection': 'keep-alive',
                'Referer': 'https://www.songkick.com/',
                'Upgrade-Insecure-Requests': '1'
            }

            try:
                response = requests.get(url, headers=headers, timeout=25)
                response.raise_for_status()
            except requests.Timeout as e:
                logger.error(f"Songkick {market}: TIMEOUT après 25 secondes - {e}")
                return []
            except requests.ConnectionError as e:
                logger.error(f"Songkick {market}: CONNECTION ERROR - {e}")
                return []
            except Exception as e:
                logger.error(f"Songkick {market}: HTTP ERROR ({type(e).__name__}): {e}")
                return []

            page_size = len(response.text)
            logger.info(f"Songkick {market}: Page chargée ({page_size} chars, status {response.status_code})")

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            all_links = soup.find_all('a', href=True)
            logger.info(f"Songkick {market}: {len(all_links)} total <a> tags trouvés")

            # Filter concert links
            events_elements = []
            for link in all_links:
                href = link.get('href', '')
                if "/concerts/" in href and "-" in href.split("/concerts/")[-1]:
                    events_elements.append(link)

            logger.info(f"Songkick {market}: {len(events_elements)} liens de concerts trouvés avec pattern /concerts/ID-NAME")

            parsed_count = 0
            for link_idx, link_elem in enumerate(events_elements):
                try:
                    title = link_elem.get_text(strip=True) if link_elem.get_text(strip=True) else "Unknown"
                    url = link_elem.get('href', '')

                    # Nettoyer le titre
                    if title:
                        title = title.split('\n')[0][:200]

                    is_sold_out = "sold out" in title.lower()

                    event = {
                        "title": title,
                        "date": "Date unknown",
                        "market": market,
                        "platform": "Songkick",
                        "url": url,
                        "sold_out": is_sold_out,
                        "scraped_at": datetime.now().isoformat()
                    }

                    # Garder TOUS les événements
                    if title and title != "Unknown" and len(title) > 3:
                        events.append(event)
                        parsed_count += 1
                        logger.info(f"✓ {market} Songkick: {title}")
                    else:
                        if link_idx < 3:
                            logger.warning(f"Skipped link [{link_idx}]: title='{title}' (len={len(title)})")

                except Exception as e:
                    if link_idx < 3:
                        logger.warning(f"Erreur parsing lien Songkick [{link_idx}]: {e}")
                    continue

            logger.info(f"Songkick {market}: Traité {len(events_elements)} liens, {parsed_count} événements valides trouvés")

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

            # Configuration ChromeDriver
            driver = None
            try:
                # Essayer avec webdriver-manager
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                logger.info(f"✓ Chrome initialized with webdriver-manager")
            except Exception as e:
                logger.warning(f"WebDriver manager failed: {e}")
                try:
                    # Essayer sans service (utilise Chrome depuis le PATH ou env var)
                    driver = webdriver.Chrome(options=options)
                    logger.info(f"✓ Chrome initialized without service (using PATH)")
                except Exception as e2:
                    logger.error(f"Failed to initialize Chrome at all: {e2}")
                    raise

            if not driver:
                raise Exception("Failed to initialize Chrome WebDriver")

            url = market_config['viagogo_url']
            logger.info(f"Accès à: {url}")
            driver.get(url)

            # Attendre que la page se charge complètement (JavaScript)
            wait_time = 8
            logger.info(f"Viagogo {market}: Attente de {wait_time}s pour le chargement JS...")
            time.sleep(wait_time)

            # Vérifier le chargement
            page_size = len(driver.page_source)
            logger.info(f"Viagogo {market}: Page chargée ({page_size} chars), recherche des éléments...")

            # Chercher les liens de concerts (stratégie robuste)
            # Viagogo utilise des URLs comme /Concert-Tickets/Genre/Artist-Tickets
            all_links = driver.find_elements(By.TAG_NAME, "a")
            logger.info(f"Viagogo {market}: {len(all_links)} total <a> tags trouvés")

            # DEBUG: Montrer les premiers liens
            if len(all_links) > 0:
                sample_links = []
                for i, link in enumerate(all_links[:5]):
                    href = link.get_attribute("href") or ""
                    sample_links.append(href[:80])
                logger.info(f"Viagogo {market}: Premier lien: {sample_links[0] if sample_links else 'N/A'}")

            events_elements = []

            for link in all_links:
                href = link.get_attribute("href") or ""
                if "/Concert-Tickets/" in href:
                    events_elements.append(link)

            logger.info(f"Viagogo {market}: {len(events_elements)} liens de concerts trouvés avec pattern /Concert-Tickets/")

            parsed_count = 0
            for link_idx, link_elem in enumerate(events_elements):
                try:
                    url = link_elem.get_attribute("href") or ""

                    # Essayer d'extraire le titre du texte du lien
                    title = link_elem.text.strip() if link_elem.text else ""

                    # Si pas de texte, extraire du URL (/Concert-Tickets/Genre/Artist-Tickets)
                    if not title or title == "Unknown":
                        parts = url.split("/Concert-Tickets/")
                        if len(parts) > 1:
                            artist_part = parts[1].split("/")[-1]  # Dernier segment
                            title = artist_part.replace("-Tickets", "").replace("-", " ")

                    # Nettoyer le titre
                    if title:
                        title = title.split('\n')[0][:200]  # Première ligne, max 200 chars

                    is_sold_out = "sold out" in title.lower() or \
                                 "ausverkauft" in title.lower() or \
                                 "épuisé" in title.lower()

                    event = {
                        "title": title,
                        "date": "Date unknown",
                        "market": market,
                        "platform": "Viagogo",
                        "url": url,
                        "sold_out": is_sold_out,
                        "scraped_at": datetime.now().isoformat()
                    }

                    # Garder TOUS les événements
                    if title and title != "Unknown" and len(title) > 3:
                        events.append(event)
                        parsed_count += 1
                        logger.info(f"✓ {market} Viagogo: {title}")
                    else:
                        # Log why this link was skipped
                        if link_idx < 3:  # Only log first few
                            logger.warning(f"Skipped link [{link_idx}]: title='{title}' (len={len(title)}) url={url[:100]}")

                except Exception as e:
                    if link_idx < 3:  # Only log first few errors
                        logger.warning(f"Erreur parsing lien Viagogo [{link_idx}]: {e}")
                    continue

            logger.info(f"Viagogo {market}: Traité {len(events_elements)} liens, {parsed_count} événements valides trouvés")

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
