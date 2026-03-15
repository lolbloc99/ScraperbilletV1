# 🎵 Concert Scraper - Sold Out Detector

Scraper automatisé pour détecter les concerts et événements **sold out** sur Songkick et Viagogo dans 6 marchés européens.

## 📋 Features

✅ Scrape **Songkick** et **Viagogo**
✅ Support de 6 marchés: 🇬🇧 UK, 🇫🇷 France, 🇩🇰 Danemark, 🇸🇪 Suède, 🇮🇹 Italie, 🇪🇸 Espagne
✅ Détection automatique des **sold out**
✅ Base de données locale (évite les doublons)
✅ Logging complet
✅ Prêt pour intégration Telegram

## 🚀 Installation

### Prérequis
- Python 3.8+
- Chrome/Chromium installé
- 2-3 GB d'espace disque pour la DB

### Étapes

```bash
# 1. Cloner/copier les fichiers
cd concert_scraper

# 2. Exécuter le setup
bash setup.sh

# 3. Activer l'environnement virtuel
source venv/bin/activate  # sur macOS/Linux
# ou sur Windows:
# venv\Scripts\activate

# 4. Lancer le scraper
python3 scraper.py
```

## 📝 Configuration

Éditer `config.json` pour personnaliser:

```json
{
  "scrape_settings": {
    "timeout": 30,           // Timeout par requête (secondes)
    "delay_between_requests": 2,  // Délai entre requêtes (secondes)
    "headless": true         // Exécuter sans interface
  },
  "notification_time": "12:00"  // Heure de notification quotidienne
}
```

## 📂 Structure des fichiers

```
concert_scraper/
├── scraper.py              # Script principal de scraping
├── config.json             # Configuration
├── requirements.txt        # Dépendances Python
├── setup.sh               # Script d'installation
├── README.md              # Ce fichier
├── scraper.log            # Logs d'exécution
└── events_db.json         # Base de données des événements
```

## 🔄 Utilisation

### Exécution manuelle unique

```bash
source venv/bin/activate
python3 scraper.py
```

### Résultat typique

```
============================================================
DÉMARRAGE DU SCRAPING - 2026-03-15 12:00:00
============================================================

📍 Marché: UK
✓ UK Songkick: Coldplay at O2 Arena - SOLD OUT
✨ NOUVEAU: UK - Coldplay at O2 Arena

📍 Marché: France
✓ France Viagogo: Daft Punk Reunion - SOLD OUT
✨ NOUVEAU: France - Daft Punk Reunion

[...]

============================================================
RÉSUMÉ:
  Total événements scraped: 45
  Nouveaux événements: 12
============================================================
```

## 📊 Structure de la base de données

```json
{
  "events": {
    "a3f8d9c2b1e4f6a7c9d2e1f4": {
      "title": "Coldplay at O2 Arena",
      "date": "15 Mar 2026",
      "market": "UK",
      "platform": "Songkick",
      "url": "https://www.songkick.com/concerts/...",
      "sold_out": true,
      "scraped_at": "2026-03-15T12:00:00"
    }
  },
  "last_updated": "2026-03-15T12:00:00"
}
```

## 🌐 Déploiement

### Options de déploiement

1. **Mode Local JSON** (défaut)
   - Fichiers JSON locaux
   - Idéal pour tester
   - `python3 scraper.py`

2. **Mode MongoDB Local**
   - Base de données MongoDB en local
   - `python3 scraper_mongodb.py`
   - Nécessite MongoDB installé

3. **Mode Cloud - Railway + MongoDB Atlas** ⭐ (RECOMMANDÉ)
   - Déploiement 24/7 sur Railway
   - Base de données MongoDB Atlas (cloud)
   - Scraping automatique quotidien
   - API REST accessible
   - **Gratuit!** 🎉

👉 **[Guide complet Railway + MongoDB](./RAILWAY_DEPLOYMENT.md)**

👉 **[Comparaison des options](./DEPLOYMENT_OPTIONS.md)**

## 📁 Fichiers de déploiement

```
├── scraper.py                 # Scraper local (JSON)
├── scraper_mongodb.py         # Scraper MongoDB
├── main.py                    # Point d'entrée Railway (avec scheduler)
├── Dockerfile                 # Pour Railway
├── railway.json               # Config Railway
├── .env.example               # Variables d'environnement
├── RAILWAY_DEPLOYMENT.md      # Guide de déploiement
└── DEPLOYMENT_OPTIONS.md      # Comparaison des modes
```

## 🔗 Prochaine étape: Telegram

Une fois le scraper déployé (local ou cloud), on intègrera la notification Telegram avec:
- Alerte quotidienne à 12h
- Résumé de tous les sold out trouvés
- Lien direct vers les événements

## ⚠️ Notes importantes

1. **Rate limiting**: Le scraper respecte les délais entre requêtes
2. **Légalité**: Vérifiez les ToS de Songkick/Viagogo pour votre région
3. **Performance**: Sur une machine locale, le scraping prend ~2-5 minutes
4. **Maintenance**: Nettoyer `events_db.json` tous les 3-6 mois

## 🐛 Troubleshooting

**Erreur ChromeDriver?**
```bash
# Installer manuellement
# macOS:
brew install chromedriver

# Linux:
sudo apt-get install chromium-chromedriver

# Windows: Télécharger depuis https://chromedriver.chromium.org/
```

**Selenium timeout?**
- Augmenter `timeout` et `delay_between_requests` dans `config.json`
- Vérifier la connexion internet
- Essayer avec un VPN si bloqué par région

## 📧 Support

Pour des questions ou bugs, vérifiez:
- `scraper.log` pour les détails
- La configuration dans `config.json`
- La connexion internet et l'accès aux sites

---

**Prêt pour Telegram?** Dis-moi! 🚀
