# 🚀 Démarrage Rapide

Lancez le scraper en 3 étapes!

## 1️⃣ Installation (2 min)

```bash
# MacOS
bash setup.sh

# Linux
bash setup.sh

# Windows (PowerShell)
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## 2️⃣ Test de configuration (30 sec)

```bash
# Vérifier que tout fonctionne
make test

# Ou manuellement
source venv/bin/activate
python3 test_scraper.py
```

## 3️⃣ Lancer le scraper! 🎵

```bash
make run

# Ou manuellement
source venv/bin/activate
python3 scraper.py
```

## 📊 Voir les résultats

```bash
# Afficher tous les événements
make view

# Afficher seulement les nouveaux du jour
make view-new

# Afficher les logs
make logs
```

---

## ⚡ Commandes rapides

```bash
make install     # Installation
make test        # Test
make run         # Lancer
make view        # Voir résultats
make logs        # Logs
make clean       # Nettoyer
make help        # Aide
```

---

## 🔧 Configuration personnalisée

Éditez `config.json` pour:
- Ajouter/retirer des marchés
- Changer les délais entre requêtes
- Modifier l'URL de notification (quand Telegram sera intégré)

```json
{
  "markets": {
    "UK": { ... },
    "France": { ... }
  },
  "scrape_settings": {
    "delay_between_requests": 2
  }
}
```

---

## 🎯 Prochaine étape

Une fois que ça marche:

```
✅ Scraper fonctionne?
✅ Événements détectés?
✅ DB créée?

→ Prochaine: Intégration Telegram! 🤖
```

---

## ⚠️ Problèmes courants

**ChromeDriver not found?**
- macOS: `brew install chromedriver`
- Linux: `sudo apt-get install chromium-chromedriver`

**Selenium timeout?**
- Augmentez `timeout` dans `config.json`
- Vérifiez votre connexion internet

**Besoin d'aide?**
- Vérifiez `scraper.log`
- Lancez `python3 test_scraper.py` pour diagnostiquer

---

**C'est bon?** Dis-moi et on passe à Telegram! 🚀
