#!/usr/bin/env python3
"""
MINIMAL SCRAPER TEST - Reproduction exacte de la logique du scraper
Avec logging maximal pour débuger
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Load config
with open('config.json') as f:
    config = json.load(f)

print("\n" + "="*80)
print("🧪 MINIMAL SCRAPER TEST - Reproduction exacte de la logique")
print("="*80 + "\n")

def test_songkick_exact():
    """Test exact de la logique Songkick du scraper"""
    print("🎵 SONGKICK TEST")
    print("-" * 80)

    market = "UK"
    market_config = config['markets'][market]
    url = market_config['songkick_url']

    print(f"URL: {url}\n")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(options=options)

    try:
        # Étape 1: Charger la page
        print("Étape 1: Charger la page...")
        driver.get(url)
        print(f"  ✓ Page requested")

        # Étape 2: Attendre le chargement JS
        print(f"\nÉtape 2: Attendre 5 secondes pour JS...")
        time.sleep(5)
        print(f"  ✓ Attente complétée")

        # Étape 3: Vérifier que la page s'est chargée
        print(f"\nÉtape 3: Vérifier le chargement...")
        body_text = driver.find_element(By.TAG_NAME, "body").text
        page_source = driver.page_source
        print(f"  ✓ Body text: {len(body_text)} chars")
        print(f"  ✓ Page source: {len(page_source)} chars")
        print(f"  ✓ Title: {driver.title}")

        # Étape 4: Trouver TOUS les liens
        print(f"\nÉtape 4: Chercher tous les <a> tags...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"  ✓ Total <a> tags: {len(all_links)}")

        if len(all_links) == 0:
            print(f"  ❌ PROBLÈME: Aucun <a> tag trouvé!")
            print(f"     Cela signifie que la page ne charge pas correctement")
            return

        # Étape 5: Filtrer les liens de concerts
        print(f"\nÉtape 5: Filtrer les liens /concerts/...")
        concert_links = []

        for i, link in enumerate(all_links):
            href = link.get_attribute("href") or ""
            text = link.text.strip() if link.text else ""

            # Vérifier le pattern
            if "/concerts/" in href:
                # Vérifier qu'il y a un ID après /concerts/
                concert_part = href.split("/concerts/")[-1]
                if "-" in concert_part:
                    concert_links.append(link)

                    # Afficher les détails
                    if len(concert_links) <= 10:
                        print(f"\n  [{i}] Trouvé!")
                        print(f"      Text: {text[:100]}")
                        print(f"      Href: {href[:100]}")

        print(f"\n  ✓ Total liens /concerts/: {len(concert_links)}")

        if len(concert_links) == 0:
            print(f"  ❌ PROBLÈME: Aucun lien /concerts/ trouvé!")
            print(f"     Les liens trouvés ne matchent pas le pattern /concerts/ID-NAME")

            # Afficher les premiers liens pour débuger
            print(f"\n  DEBUG: Premiers 20 liens trouvés:")
            for i, link in enumerate(all_links[:20]):
                href = link.get_attribute("href") or ""
                text = link.text.strip()[:30] if link.text else ""
                print(f"    [{i}] {text} -> {href[:80]}")

            return

        # Étape 6: Extraire les événements
        print(f"\nÉtape 6: Extraire les événements...")
        events = []

        for link_elem in concert_links:
            try:
                title = link_elem.text.strip() if link_elem.text else "Unknown"
                url = link_elem.get_attribute("href") or ""

                # Nettoyer le titre
                if title:
                    title = title.split('\n')[0][:200]

                # Vérifier qu'il est valide
                if title and title != "Unknown" and len(title) > 3:
                    events.append({
                        "title": title,
                        "url": url
                    })

                    if len(events) <= 10:
                        print(f"  ✓ {title}")

            except Exception as e:
                print(f"  ! Erreur parsing: {e}")

        print(f"\n  ✓ Total événements extraits: {len(events)}")

        if len(events) == 0 and len(concert_links) > 0:
            print(f"  ❌ PROBLÈME: Liens trouvés ({len(concert_links)}) mais 0 événements!")
            print(f"     Cela signifie qu'aucun lien n'a un titre valide")

    finally:
        driver.quit()


def test_viagogo_exact():
    """Test exact de la logique Viagogo du scraper"""
    print("\n" + "="*80)
    print("🎫 VIAGOGO TEST")
    print("-" * 80)

    market = "UK"
    market_config = config['markets'][market]
    url = market_config['viagogo_url']

    print(f"URL: {url}\n")

    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=options)
    except:
        driver = webdriver.Chrome(options=options)

    try:
        # Étape 1: Charger la page
        print("Étape 1: Charger la page...")
        driver.get(url)
        print(f"  ✓ Page requested")

        # Étape 2: Attendre le chargement JS
        print(f"\nÉtape 2: Attendre 5 secondes pour JS...")
        time.sleep(5)
        print(f"  ✓ Attente complétée")

        # Étape 3: Vérifier que la page s'est chargée
        print(f"\nÉtape 3: Vérifier le chargement...")
        body_text = driver.find_element(By.TAG_NAME, "body").text
        page_source = driver.page_source
        print(f"  ✓ Body text: {len(body_text)} chars")
        print(f"  ✓ Page source: {len(page_source)} chars")
        print(f"  ✓ Title: {driver.title}")

        # Étape 4: Trouver TOUS les liens
        print(f"\nÉtape 4: Chercher tous les <a> tags...")
        all_links = driver.find_elements(By.TAG_NAME, "a")
        print(f"  ✓ Total <a> tags: {len(all_links)}")

        if len(all_links) == 0:
            print(f"  ❌ PROBLÈME: Aucun <a> tag trouvé!")
            return

        # Étape 5: Filtrer les liens de concerts
        print(f"\nÉtape 5: Filtrer les liens /Concert-Tickets/...")
        concert_links = []

        for i, link in enumerate(all_links):
            href = link.get_attribute("href") or ""
            text = link.text.strip() if link.text else ""

            if "/Concert-Tickets/" in href:
                concert_links.append(link)

                if len(concert_links) <= 10:
                    print(f"\n  [{i}] Trouvé!")
                    print(f"      Text: {text[:100]}")
                    print(f"      Href: {href[:100]}")

        print(f"\n  ✓ Total liens /Concert-Tickets/: {len(concert_links)}")

        if len(concert_links) == 0:
            print(f"  ❌ PROBLÈME: Aucun lien /Concert-Tickets/ trouvé!")

            print(f"\n  DEBUG: Premiers 20 liens trouvés:")
            for i, link in enumerate(all_links[:20]):
                href = link.get_attribute("href") or ""
                text = link.text.strip()[:30] if link.text else ""
                print(f"    [{i}] {text} -> {href[:80]}")

            return

        # Étape 6: Extraire les événements
        print(f"\nÉtape 6: Extraire les événements...")
        events = []

        for link_elem in concert_links:
            try:
                url = link_elem.get_attribute("href") or ""
                title = link_elem.text.strip() if link_elem.text else ""

                # Si pas de texte, extraire du URL
                if not title or title == "Unknown":
                    parts = url.split("/Concert-Tickets/")
                    if len(parts) > 1:
                        artist_part = parts[1].split("/")[-1]
                        title = artist_part.replace("-Tickets", "").replace("-", " ")

                # Nettoyer le titre
                if title:
                    title = title.split('\n')[0][:200]

                # Vérifier qu'il est valide
                if title and title != "Unknown" and len(title) > 3:
                    events.append({
                        "title": title,
                        "url": url
                    })

                    if len(events) <= 10:
                        print(f"  ✓ {title}")

            except Exception as e:
                print(f"  ! Erreur parsing: {e}")

        print(f"\n  ✓ Total événements extraits: {len(events)}")

        if len(events) == 0 and len(concert_links) > 0:
            print(f"  ❌ PROBLÈME: Liens trouvés ({len(concert_links)}) mais 0 événements!")

    finally:
        driver.quit()


# Run tests
test_songkick_exact()
test_viagogo_exact()

print("\n" + "="*80)
print("✅ TEST TERMINÉ")
print("="*80)
print("\nLes résultats ci-dessus montrent exactement où le problème se trouve:")
print("  - Si 'Aucun <a> tag': Chrome ne charge pas la page")
print("  - Si 'Aucun lien /concerts/': Les liens n'ont pas ce pattern")
print("  - Si 'Liens trouvés mais 0 événements': Les titres sont vides ou trop courts\n")
