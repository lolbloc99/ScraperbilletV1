#!/usr/bin/env python3
"""
Main entry point for Railway deployment
Gère l'ordonnancement des tâches et expose une API pour les healthchecks
"""

import os
import logging
from datetime import datetime, time
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask import Flask, jsonify, render_template
from scraper_mongodb import ConcertScraperMongoDB
import json

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Variables globales
last_run = None
last_result = None
scheduler = None

# Flask app pour Railway
app = Flask(__name__, template_folder='templates')

@app.route('/', methods=['GET'])
def index():
    """Serve the web interface"""
    return render_template('index.html')

@app.route('/logs', methods=['GET'])
def logs():
    """Serve the logs page"""
    return render_template('logs.html')

@app.route('/test', methods=['GET'])
def test():
    """Serve the test page"""
    return render_template('test.html')

@app.route('/health', methods=['GET'])
def health():
    """Health check pour Railway"""
    return jsonify({
        "status": "ok",
        "last_run": last_run,
        "last_result": last_result
    }), 200

@app.route('/stats', methods=['GET'])
def stats():
    """Obtenir les statistiques"""
    try:
        scraper = ConcertScraperMongoDB()
        stats = scraper.db.get_statistics()
        scraper.close()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/events', methods=['GET'])
def get_events():
    """Récupérer les événements récents"""
    try:
        scraper = ConcertScraperMongoDB()
        events = scraper.db.get_new_events(hours=24)
        scraper.close()
        return jsonify({
            "count": len(events),
            "events": events
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/test-http', methods=['GET'])
def test_http():
    """Test HTTP requests without Selenium"""
    import requests
    from bs4 import BeautifulSoup

    result = {}

    try:
        # Test Songkick with proper headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Referer': 'https://www.songkick.com/',
            'Upgrade-Insecure-Requests': '1'
        }

        resp = requests.get("https://www.songkick.com/concerts", headers=headers, timeout=10)
        result['songkick_status'] = resp.status_code
        result['songkick_size'] = len(resp.text)
        result['songkick_has_concerts'] = "/concerts/" in resp.text
        result['songkick_links_count'] = resp.text.count("<a ")

        # Parse and count concert links properly
        soup = BeautifulSoup(resp.text, 'html.parser')
        all_links = soup.find_all('a', href=True)
        concert_links = [l for l in all_links if "/concerts/" in l.get('href', '') and "-" in l.get('href', '').split("/concerts/")[-1]]
        result['songkick_concert_links'] = len(concert_links)
    except Exception as e:
        result['songkick_error'] = str(e)
        import traceback
        result['songkick_traceback'] = traceback.format_exc()

    try:
        # Test Viagogo
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }
        resp = requests.get("https://www.viagogo.com/", headers=headers, timeout=10)
        result['viagogo_status'] = resp.status_code
        result['viagogo_size'] = len(resp.text)
        result['viagogo_has_concerts'] = "/Concert-Tickets/" in resp.text
        result['viagogo_links_count'] = resp.text.count("<a ")
    except Exception as e:
        result['viagogo_error'] = str(e)
        import traceback
        result['viagogo_traceback'] = traceback.format_exc()

    return jsonify(result), 200


@app.route('/test-scraper', methods=['GET'])
def test_scraper():
    """Test the actual scraper directly"""
    import json as json_module

    result = {
        "songkick_test": {},
        "viagogo_test": {},
        "full_scrape": {}
    }

    try:
        scraper = ConcertScraperMongoDB()
        logger.info("✓ Scraper created successfully")

        # Test Songkick
        try:
            events = scraper.scrape_songkick("UK", scraper.config['markets']['UK'])
            result['songkick_test']['events_found'] = len(events)
            result['songkick_test']['success'] = True
            if events:
                result['songkick_test']['sample'] = events[0]
            logger.info(f"✓ Songkick test: {len(events)} events found")
        except Exception as e:
            result['songkick_test']['success'] = False
            result['songkick_test']['error'] = str(e)
            import traceback
            result['songkick_test']['traceback'] = traceback.format_exc()
            logger.error(f"✗ Songkick test failed: {e}")

        # Test Viagogo
        try:
            events = scraper.scrape_viagogo("UK", scraper.config['markets']['UK'])
            result['viagogo_test']['events_found'] = len(events)
            result['viagogo_test']['success'] = True
            if events:
                result['viagogo_test']['sample'] = events[0]
            logger.info(f"✓ Viagogo test: {len(events)} events found")
        except Exception as e:
            result['viagogo_test']['success'] = False
            result['viagogo_test']['error'] = str(e)
            import traceback
            result['viagogo_test']['traceback'] = traceback.format_exc()
            logger.error(f"✗ Viagogo test failed: {e}")

        # Full scrape
        try:
            all_events = scraper.run_scrape_all_markets()
            result['full_scrape']['total_events'] = len(all_events)
            result['full_scrape']['success'] = True
            logger.info(f"✓ Full scrape: {len(all_events)} events found")
        except Exception as e:
            result['full_scrape']['success'] = False
            result['full_scrape']['error'] = str(e)
            import traceback
            result['full_scrape']['traceback'] = traceback.format_exc()
            logger.error(f"✗ Full scrape failed: {e}")

        scraper.close()

    except Exception as e:
        result['error'] = str(e)
        import traceback
        result['traceback'] = traceback.format_exc()
        logger.error(f"✗ Scraper test failed: {e}")

    return jsonify(result), 200


@app.route('/debug', methods=['GET'])
def debug_selenium():
    """Endpoint pour déboguer Selenium sur Railway"""
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
    import time as time_module

    debug_info = {}

    try:
        # Test Chrome initialization
        logger.info("🔧 [DEBUG] Initializing Chrome...")
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')

        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            debug_info['chrome_status'] = "✓ Chrome initialized with webdriver-manager"
        except Exception as e:
            driver = webdriver.Chrome(options=options)
            debug_info['chrome_status'] = f"Chrome initialized without service (fallback)"

        # Test Songkick
        logger.info("🔧 [DEBUG] Testing Songkick...")
        driver.get("https://www.songkick.com/concerts")
        time_module.sleep(8)

        all_links = driver.find_elements(By.TAG_NAME, "a")
        page_size = len(driver.page_source)

        debug_info['songkick'] = {
            'page_size': page_size,
            'total_links': len(all_links),
            'sample_links': [link.get_attribute("href")[:80] for link in all_links[:3]],
            'concerts_pattern_found': sum(1 for link in all_links if "/concerts/" in (link.get_attribute("href") or ""))
        }

        # Test Viagogo
        logger.info("🔧 [DEBUG] Testing Viagogo...")
        driver.get("https://www.viagogo.com/")
        time_module.sleep(8)

        all_links = driver.find_elements(By.TAG_NAME, "a")
        page_size = len(driver.page_source)

        debug_info['viagogo'] = {
            'page_size': page_size,
            'total_links': len(all_links),
            'sample_links': [link.get_attribute("href")[:80] for link in all_links[:3]],
            'concert_tickets_pattern_found': sum(1 for link in all_links if "/Concert-Tickets/" in (link.get_attribute("href") or ""))
        }

        driver.quit()

        return jsonify(debug_info), 200

    except Exception as e:
        logger.error(f"Debug endpoint error: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@app.route('/run', methods=['POST'])
def run_now():
    """Déclencher le scraping immédiatement"""
    global last_run, last_result

    try:
        logger.info("🚀 Scraping déclenché manuellement")
        logger.info(f"   MongoDB URI: {os.getenv('MONGODB_URI', 'NOT SET')[:50]}...")

        scraper = ConcertScraperMongoDB()
        logger.info(f"✓ Scraper créé avec succès")

        result = scraper.execute()
        logger.info(f"✓ Scraping exécuté: {result.get('total_events', '?')} événements")

        scraper.close()

        last_run = datetime.now().isoformat()
        last_result = result

        return jsonify(result), 200
    except Exception as e:
        logger.error(f"❌ Erreur scraping: {e}", exc_info=True)
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


def scrape_job():
    """Job de scraping planifié"""
    global last_run, last_result

    try:
        logger.info("🔄 Exécution du scraping planifiée")
        scraper = ConcertScraperMongoDB()
        result = scraper.execute()
        scraper.close()

        last_run = datetime.now().isoformat()
        last_result = result

        logger.info(f"✅ Scraping terminé: {result.get('new_events', 0)} nouveaux événements")

    except Exception as e:
        logger.error(f"❌ Erreur scraping: {e}")
        last_result = {"error": str(e)}


def start_scheduler():
    """Démarrer le scheduler"""
    global scheduler

    scheduler = BackgroundScheduler()

    # Lire la configuration
    with open('config.json', 'r') as f:
        config = json.load(f)

    notification_time = config.get('notification_time', '12:00')
    hour, minute = map(int, notification_time.split(':'))

    # Ajouter le job récurrent
    scheduler.add_job(
        scrape_job,
        CronTrigger(hour=hour, minute=minute),
        id='daily_scrape',
        name='Daily Concert Scraping',
        replace_existing=True
    )

    logger.info(f"⏰ Scraping planifié pour {notification_time} chaque jour")

    # Optionnel: scraper au démarrage après 10 secondes
    scheduler.add_job(
        scrape_job,
        'date',
        run_date=datetime.now().replace(second=10),
        id='startup_scrape',
        name='Initial Scrape',
        replace_existing=True
    )

    scheduler.start()
    logger.info("✅ Scheduler démarré")


def main():
    """Point d'entrée principal"""

    # Afficher la configuration
    logger.info("=" * 60)
    logger.info("🎵 Concert Scraper - Railway Edition")
    logger.info("=" * 60)

    # Vérifier MongoDB
    mongodb_uri = os.getenv('MONGODB_URI')
    if not mongodb_uri:
        logger.warning("⚠️  MONGODB_URI non défini - utilisant valeur par défaut locale")
        mongodb_uri = 'mongodb://localhost:27017/scraperbillet'

    logger.info(f"📦 Base de données: {mongodb_uri.split('@')[0]}...****")

    # Démarrer le scheduler
    start_scheduler()

    # Obtenir le port de Railway
    port = int(os.getenv('PORT', 5000))

    logger.info(f"🚀 API Flask démarrée sur port {port}")
    logger.info("=" * 60)

    # Démarrer l'API Flask
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        use_reloader=False
    )


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n🛑 Arrêt du service...")
        if scheduler:
            scheduler.shutdown()
