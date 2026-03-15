#!/usr/bin/env python3
"""
SAVE ACTUAL HTML - Sauvegarde le HTML réel que le scraper reçoit
Ceci est le diagnostic CRUCIAL pour comprendre ce qui se passe
"""

import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

print("\n" + "="*80)
print("💾 SAVE ACTUAL HTML - Sauvegarde du HTML réel que Selenium reçoit")
print("="*80 + "\n")

# Load config
with open('config.json') as f:
    config = json.load(f)

def save_songkick_html():
    """Sauvegarde le HTML de Songkick"""
    print("🎵 SONGKICK")
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
        driver.get(url)
        time.sleep(6)

        # Get the actual HTML
        html = driver.page_source
        body_text = driver.find_element(By.TAG_NAME, "body").text

        # Save to file
        with open('songkick_actual_html.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ HTML sauvegardé: songkick_actual_html.html")
        print(f"   Size: {len(html)} chars")
        print(f"   Body text: {len(body_text)} chars")

        # Analyse rapide
        print(f"\n📊 Analyse rapide:")
        print(f"   Contient 'concert': {'concert' in html.lower()}")
        print(f"   Contient 'event': {'event' in html.lower()}")
        print(f"   Nombre de <a> tags: {html.count('<a ')}")
        print(f"   Nombre de 'href=': {html.count('href=')}")

        # Chercher les patterns spécifiquement
        print(f"\n🔍 Patterns recherchés:")
        print(f"   '/concerts/' found: {'/concerts/' in html}")

        # Montrer les <a> tags qui contiennent /concerts/
        import re
        concerts_links = re.findall(r'<a[^>]*href="([^"]*concerts[^"]*)"[^>]*>', html, re.IGNORECASE)
        print(f"   <a> avec /concerts/: {len(concerts_links)}")
        for link in concerts_links[:5]:
            print(f"      - {link[:100]}")

    finally:
        driver.quit()


def save_viagogo_html():
    """Sauvegarde le HTML de Viagogo"""
    print("\n" + "="*80)
    print("🎫 VIAGOGO")
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
        driver.get(url)
        time.sleep(6)

        # Get the actual HTML
        html = driver.page_source
        body_text = driver.find_element(By.TAG_NAME, "body").text

        # Save to file
        with open('viagogo_actual_html.html', 'w', encoding='utf-8') as f:
            f.write(html)

        print(f"✅ HTML sauvegardé: viagogo_actual_html.html")
        print(f"   Size: {len(html)} chars")
        print(f"   Body text: {len(body_text)} chars")

        # Analyse rapide
        print(f"\n📊 Analyse rapide:")
        print(f"   Contient 'concert': {'concert' in html.lower()}")
        print(f"   Contient 'ticket': {'ticket' in html.lower()}")
        print(f"   Nombre de <a> tags: {html.count('<a ')}")
        print(f"   Nombre de 'href=': {html.count('href=')}")

        # Chercher les patterns spécifiquement
        print(f"\n🔍 Patterns recherchés:")
        print(f"   '/Concert-Tickets/' found: {'/Concert-Tickets/' in html}")

        # Montrer les <a> tags qui contiennent /Concert-Tickets/
        import re
        tickets_links = re.findall(r'<a[^>]*href="([^"]*Concert-Tickets[^"]*)"[^>]*>', html, re.IGNORECASE)
        print(f"   <a> avec /Concert-Tickets/: {len(tickets_links)}")
        for link in tickets_links[:5]:
            print(f"      - {link[:100]}")

    finally:
        driver.quit()


# Run
try:
    save_songkick_html()
except Exception as e:
    print(f"❌ Erreur Songkick: {e}")

try:
    save_viagogo_html()
except Exception as e:
    print(f"❌ Erreur Viagogo: {e}")

print("\n" + "="*80)
print("✅ SAVE COMPLETE")
print("="*80)
print("\nFichiers créés:")
print("  - songkick_actual_html.html (HTML brut de Songkick)")
print("  - viagogo_actual_html.html (HTML brut de Viagogo)")
print("\nOuvrez ces fichiers dans un navigateur pour voir exactement")
print("ce que le scraper reçoit et cherchez les patterns:")
print("  - /concerts/ pour Songkick")
print("  - /Concert-Tickets/ pour Viagogo\n")
