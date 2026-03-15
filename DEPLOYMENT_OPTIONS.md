# 🚀 Options de déploiement

ScraperbilletV1 supporte 3 modes de déploiement:

## 1️⃣ Mode Local - JSON File (par défaut)

**Utilise**: Fichiers JSON locaux
**Idéal pour**: Tests et développement
**Coût**: 0€

```bash
# Installation
bash setup.sh

# Lancer
make run

# Voir les résultats
make view
```

**Fichier**: `scraper.py`
**Stockage**: `events_db.json` (local)

---

## 2️⃣ Mode MongoDB Local

**Utilise**: MongoDB en local + scraper MongoDB
**Idéal pour**: Développement avec vrai DB
**Coût**: 0€ + serveur local

### Installation

```bash
# 1. Installer MongoDB
# macOS:
brew install mongodb-community

# Linux:
sudo apt-get install mongodb

# 2. Démarrer MongoDB
mongod

# 3. Installer dépendances
pip install -r requirements.txt

# 4. Lancer le scraper
python3 scraper_mongodb.py
```

**Fichier**: `scraper_mongodb.py`
**Stockage**: MongoDB local (localhost:27017)

---

## 3️⃣ Mode Cloud - Railway + MongoDB Atlas ⭐ (RECOMMANDÉ)

**Utilise**: Railway (hosting) + MongoDB Atlas (cloud DB)
**Idéal pour**: Production 24/7
**Coût**: Gratuit (5$/month de crédit Railway + MongoDB gratuit)

### Avantages
✅ Toujours actif (24/7)
✅ Scraping automatique chaque jour
✅ API REST accessible de partout
✅ Base de données cloud
✅ Monitoring et logs

### Installation
👉 Voir **[RAILWAY_DEPLOYMENT.md](./RAILWAY_DEPLOYMENT.md)**

---

## 📊 Comparaison

| Feature | JSON Local | MongoDB Local | Railway + Atlas |
|---------|-----------|---------------|-----------------|
| Démarrage facile | ✅ | ⚠️ | ✅ |
| Gratuit | ✅ | ✅ | ✅ |
| 24/7 actif | ❌ | ❌ | ✅ |
| Scraping auto | ❌ | ❌ | ✅ |
| API REST | ❌ | ❌ | ✅ |
| Scalabilité | ❌ | ⚠️ | ✅ |
| Production ready | ❌ | ⚠️ | ✅ |

---

## 🎯 Recommandation

**Pour débuter**: Mode 1 (JSON Local) ➜ `make run`
**Pour tester DB**: Mode 2 (MongoDB Local) ➜ `python3 scraper_mongodb.py`
**Pour production**: Mode 3 (Railway + Atlas) ➜ Voir guide Railway

---

## 🔄 Migrer d'un mode à l'autre

### JSON → MongoDB (local ou cloud)

Les données JSON seront perdues. Pour les garder:

```python
# Script de migration (future feature)
# Convertir events_db.json en documents MongoDB
```

### MongoDB Local → Railway

```bash
# 1. Créer cluster MongoDB Atlas
# 2. Déployer sur Railway
# 3. Ajouter MONGODB_URI aux variables d'env
# 4. Railway synchronisera les données
```

---

**Choix ta stratégie et commence! 🚀**
