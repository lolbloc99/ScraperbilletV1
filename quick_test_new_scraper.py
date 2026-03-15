#!/usr/bin/env python3
"""
Quick test - vérifie que la nouvelle stratégie de liens fonctionne
"""

import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Load config
with open('config.json') as f:
    config = json.load(f)

print("\n" + "="*80)
print("🧪 TEST DE LA NOUVELLE STRATÉGIE (liens d'événements)")
print("="*80 + "\n")

def test_songkick():
    """Test la nouvelle stratégie Songkick"""
    print("🎵 SONGKICK - Teste la stratégie de liens /concerts/\n")

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
        url = config['markets']['UK']['songkick_url']
        print(f"URL: {url}\n")
        driver.get(url)
        time.sleep(5)

        # Chercher les liens de concerts avec le pattern /concerts/
        all_links = driver.find_elements(By.TAG_NAME, "a")
        concert_links = []

        for link in all_links:
            href = link.get_attribute("href") or ""
            if "/concerts/" in href and "-" in href.split("/concerts/")[-1]:
                concert_links.append(link)

        print(f"✅ Liens trouvés: {len(concert_links)}\n")

        # Extraire les détails
        parsed = 0
        for i, link in enumerate(concert_links[:10]):
            try:
                title = link.text.strip() if link.text else "Unknown"
                title = title.split('\n')[0][:100]
                href = link.get_attribute("href") or ""

                if title and title != "Unknown" and len(title) > 3:
                    parsed += 1
                    print(f"  {i+1}. {title}")
                    print(f"     URL: {href}\n")
            except:
                pass

        print(f"✅ Événements valides extraits: {parsed}/{len(concert_links)}")
        return parsed > 0

    finally:
        driver.quit()


def test_viagogo():
    """Test la nouvelle stratégie Viagogo"""
    print("\n🎫 VIAGOGO - Teste la stratégie de liens /Concert-Tickets/\n")

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
        url = config['markets']['UK']['viagogo_url']
        print(f"URL: {url}\n")
        driver.get(url)
        time.sleep(5)

        # Chercher les liens de concerts avec le pattern /Concert-Tickets/
        all_links = driver.find_elements(By.TAG_NAME, "a")
        concert_links = []

        for link in all_links:
            href = link.get_attribute("href") or ""
            if "/Concert-Tickets/" in href:
                concert_links.append(link)

        print(f"✅ Liens trouvés: {len(concert_links)}\n")

        # Extraire les détails
        parsed = 0
        for i, link in enumerate(concert_links[:10]):
            try:
                title = link.text.strip() if link.text else "Unknown"
                title = title.split('\n')[0][:100]
                href = link.get_attribute("href") or ""

                if title and title != "Unknown" and len(title) > 3:
                    parsed += 1
                    print(f"  {i+1}. {title}")
                    print(f"     URL: {href}\n")
            except:
                pass

        print(f"✅ Événements valides extraits: {parsed}/{len(concert_links)}")
        return parsed > 0

    finally:
        driver.quit()


if __name__ == '__main__':
    songkick_ok = test_songkick()
    viagogo_ok = test_viagogo()

    print("\n" + "="*80)
    if songkick_ok and viagogo_ok:
        print("✅ SUCCÈS! Les deux sites trouvent des événements avec la nouvelle stratégie!")
    else:
        print("⚠️  Un ou les deux sites n'ont pas trouvé assez d'événements")
    print("="*80 + "\n")
