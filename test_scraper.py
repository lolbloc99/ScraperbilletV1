#!/usr/bin/env python3
"""
Script de test du scraper
Vérifie que tout fonctionne avant d'intégrer Telegram
"""

import json
import sys
import os
from datetime import datetime

def test_config():
    """Vérifier la configuration"""
    print("🔍 Test 1: Vérification du fichier config.json...")
    if not os.path.exists('config.json'):
        print("❌ config.json not found!")
        return False
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        print(f"✓ Config trouvée avec {len(config['markets'])} marchés")
        for market in config['markets']:
            print(f"  - {market}")
        return True
    except Exception as e:
        print(f"❌ Erreur config: {e}")
        return False

def test_dependencies():
    """Vérifier les dépendances"""
    print("\n🔍 Test 2: Vérification des dépendances...")
    deps = {
        'selenium': 'Selenium WebDriver',
        'bs4': 'Beautiful Soup',
        'requests': 'Requests HTTP',
    }

    missing = []
    for module, name in deps.items():
        try:
            __import__(module)
            print(f"✓ {name}")
        except ImportError:
            print(f"❌ {name}")
            missing.append(module)

    if missing:
        print(f"\n⚠️  Dépendances manquantes: {', '.join(missing)}")
        print("Installez avec: pip install -r requirements.txt")
        return False
    return True

def test_chromedriver():
    """Vérifier ChromeDriver"""
    print("\n🔍 Test 3: Vérification de ChromeDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome(options=options)
        driver.quit()
        print("✓ ChromeDriver fonctionne")
        return True
    except Exception as e:
        print(f"❌ ChromeDriver error: {e}")
        print("\n💡 Solutions:")
        print("  macOS: brew install chromedriver")
        print("  Linux: sudo apt-get install chromium-chromedriver")
        print("  Windows: Télécharger de https://chromedriver.chromium.org/")
        return False

def test_scraper_import():
    """Tester l'import du scraper"""
    print("\n🔍 Test 4: Vérification du scraper.py...")
    try:
        from scraper import ConcertScraper
        print("✓ Scraper importé avec succès")
        return True
    except Exception as e:
        print(f"❌ Erreur import scraper: {e}")
        return False

def test_database():
    """Vérifier la création de la DB"""
    print("\n🔍 Test 5: Vérification de la base de données...")
    try:
        from scraper import ConcertScraper
        scraper = ConcertScraper()
        db_file = scraper.config['database_file']

        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                db = json.load(f)
            print(f"✓ DB trouvée avec {len(db.get('events', {}))} événements enregistrés")
        else:
            print("✓ DB sera créée au premier lancement")
        return True
    except Exception as e:
        print(f"❌ Erreur DB: {e}")
        return False

def main():
    """Exécuter tous les tests"""
    print("=" * 60)
    print("🧪 TESTS DU CONCERT SCRAPER")
    print("=" * 60)

    tests = [
        test_config,
        test_dependencies,
        test_chromedriver,
        test_scraper_import,
        test_database,
    ]

    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"❌ Erreur test: {e}")
            results.append(False)

    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    passed = sum(results)
    total = len(results)

    if passed == total:
        print(f"✅ Tous les tests passés! ({passed}/{total})")
        print("\n🚀 Prêt à lancer le scraper:")
        print("   python3 scraper.py")
        return 0
    else:
        print(f"⚠️  {total - passed} test(s) échoué(s) ({passed}/{total})")
        print("\nVérifiez les erreurs ci-dessus et réessayez.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
