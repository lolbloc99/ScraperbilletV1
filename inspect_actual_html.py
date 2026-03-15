#!/usr/bin/env python3
"""
Inspecter le HTML RÉEL qu'on reçoit pour comprendre la structure
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json

def inspect_songkick():
    """Inspecter le contenu réel de Songkick"""
    print("\n" + "="*80)
    print("🎵 SONGKICK - Inspection du HTML réel")
    print("="*80)

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
        url = "https://www.songkick.com/concerts"
        print(f"\n📍 URL: {url}\n")
        driver.get(url)
        time.sleep(5)

        # Get page HTML
        page_html = driver.page_source

        print(f"✅ Page HTML reçu: {len(page_html)} chars\n")

        # Sauvegarder le HTML
        with open('/tmp/ScraperbilletV1/songkick_full_html.html', 'w') as f:
            f.write(page_html)
        print("💾 Sauvegardé dans: songkick_full_html.html\n")

        # Analyser la structure
        print("📊 ANALYSE HTML:\n")

        # Chercher des patterns courants
        patterns = [
            ('<script', 'Script tags (JS):'),
            ('event', 'Keyword "event":'),
            ('concert', 'Keyword "concert":'),
            ('<li', 'LI elements:'),
            ('<div', 'DIV elements:'),
            ('data-', 'Data attributes:'),
            ('href=', 'Links (href):'),
        ]

        for pattern, label in patterns:
            count = page_html.lower().count(pattern.lower())
            print(f"   {label:30} {count:5}")

        # Chercher des sections d'événements
        print("\n📍 Cherchant des sections qui pourraient contenir des événements:\n")

        # Regarder les scripts inline
        import re
        scripts = re.findall(r'<script[^>]*>.*?</script>', page_html, re.DOTALL)
        print(f"   {len(scripts)} script tags trouvés")

        # Chercher des JSON dans les scripts (API data)
        json_patterns = re.findall(r'(\{[^{}]*"event[^{}]*\}|\{[^{}]*"concert[^{}]*\})', page_html, re.IGNORECASE)
        print(f"   {len(json_patterns)} JSON objects avec 'event' ou 'concert'")

        if json_patterns:
            print("\n   Exemples de JSON trouvés:")
            for i, pattern in enumerate(json_patterns[:2]):
                print(f"      {pattern[:200]}...")

        # Analyser le body text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        lines = body_text.split('\n')
        print(f"\n   Body text: {len(body_text)} chars, {len(lines)} lignes")
        print(f"\n   Premières 50 lignes du body text:")
        for i, line in enumerate(lines[:50]):
            if line.strip():
                print(f"      {i:3}: {line[:80]}")

    finally:
        driver.quit()


def inspect_viagogo():
    """Inspecter le contenu réel de Viagogo"""
    print("\n" + "="*80)
    print("🎫 VIAGOGO - Inspection du HTML réel")
    print("="*80)

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
        url = "https://www.viagogo.com/"
        print(f"\n📍 URL: {url}\n")
        driver.get(url)
        time.sleep(5)

        # Get page HTML
        page_html = driver.page_source

        print(f"✅ Page HTML reçu: {len(page_html)} chars\n")

        # Sauvegarder le HTML
        with open('/tmp/ScraperbilletV1/viagogo_full_html.html', 'w') as f:
            f.write(page_html)
        print("💾 Sauvegardé dans: viagogo_full_html.html\n")

        # Analyser la structure
        print("📊 ANALYSE HTML:\n")

        patterns = [
            ('<script', 'Script tags (JS):'),
            ('event', 'Keyword "event":'),
            ('concert', 'Keyword "concert":'),
            ('<li', 'LI elements:'),
            ('<div', 'DIV elements:'),
            ('data-', 'Data attributes:'),
            ('href=', 'Links (href):'),
        ]

        for pattern, label in patterns:
            count = page_html.lower().count(pattern.lower())
            print(f"   {label:30} {count:5}")

        print("\n📍 Cherchant des sections qui pourraient contenir des événements:\n")

        import re
        scripts = re.findall(r'<script[^>]*>.*?</script>', page_html, re.DOTALL)
        print(f"   {len(scripts)} script tags trouvés")

        json_patterns = re.findall(r'(\{[^{}]*"event[^{}]*\}|\{[^{}]*"concert[^{}]*\})', page_html, re.IGNORECASE)
        print(f"   {len(json_patterns)} JSON objects avec 'event' ou 'concert'")

        # Analyser le body text
        body_text = driver.find_element(By.TAG_NAME, "body").text
        lines = body_text.split('\n')
        print(f"\n   Body text: {len(body_text)} chars, {len(lines)} lignes")
        print(f"\n   Premières 50 lignes du body text:")
        for i, line in enumerate(lines[:50]):
            if line.strip():
                print(f"      {i:3}: {line[:80]}")

    finally:
        driver.quit()


if __name__ == '__main__':
    print("\n🔍 INSPECTION DÉTAILLÉE DU HTML REÇU")
    print("Pour comprendre pourquoi le scraper ne trouve pas d'événements\n")

    inspect_songkick()
    inspect_viagogo()

    print("\n" + "="*80)
    print("✅ Inspection complète - HTMLs sauvegardés")
    print("="*80)
