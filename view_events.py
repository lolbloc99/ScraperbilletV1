#!/usr/bin/env python3
"""
Script pour visualiser les événements trouvés
"""

import json
import os
from datetime import datetime
from collections import defaultdict

def view_events():
    """Afficher tous les événements sold out de la DB"""
    db_file = 'events_db.json'

    if not os.path.exists(db_file):
        print("❌ Aucune base de données trouvée. Lancez d'abord: python3 scraper.py")
        return

    with open(db_file, 'r', encoding='utf-8') as f:
        db = json.load(f)

    events = db.get('events', {})

    if not events:
        print("📭 Aucun événement enregistré yet")
        return

    # Grouper par marché et plateforme
    grouped = defaultdict(lambda: defaultdict(list))

    for event_hash, event in events.items():
        market = event['market']
        platform = event['platform']
        grouped[market][platform].append(event)

    # Afficher
    print("=" * 80)
    print("🎵 ÉVÉNEMENTS SOLD OUT DÉTECTÉS")
    print("=" * 80)
    print(f"\nTotal: {len(events)} événements\n")

    for market in sorted(grouped.keys()):
        print(f"\n📍 {market.upper()}")
        print("-" * 80)

        for platform in sorted(grouped[market].keys()):
            platform_events = grouped[market][platform]
            print(f"\n  {platform} ({len(platform_events)} événements)")
            print("  " + "-" * 76)

            for event in platform_events:
                print(f"\n    🎭 {event['title']}")
                print(f"       📅 {event['date']}")
                print(f"       🔗 {event['url']}")
                print(f"       ⏰ Détecté: {event['scraped_at']}")

    print("\n" + "=" * 80)
    print(f"Dernière mise à jour: {db.get('last_updated', 'Unknown')}")
    print("=" * 80)

def view_new_events():
    """Afficher les événements trouvés aujourd'hui"""
    db_file = 'events_db.json'

    if not os.path.exists(db_file):
        print("❌ Aucune base de données trouvée.")
        return

    with open(db_file, 'r', encoding='utf-8') as f:
        db = json.load(f)

    events = db.get('events', {})
    today = datetime.now().date()

    new_today = []
    for event_hash, event in events.items():
        scraped_date = datetime.fromisoformat(event['scraped_at']).date()
        if scraped_date == today:
            new_today.append(event)

    print("=" * 80)
    print(f"✨ NOUVEAUX ÉVÉNEMENTS AUJOURD'HUI ({today})")
    print("=" * 80)

    if not new_today:
        print("\n📭 Aucun nouvel événement aujourd'hui")
        return

    print(f"\n{len(new_today)} nouvel(s) événement(s):\n")

    for event in new_today:
        print(f"  🎭 {event['title']}")
        print(f"     Marché: {event['market']}")
        print(f"     Platform: {event['platform']}")
        print(f"     Date: {event['date']}")
        print(f"     🔗 {event['url']}\n")

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "--new":
        view_new_events()
    else:
        view_events()
