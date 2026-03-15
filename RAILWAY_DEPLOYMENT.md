# 🚀 Déploiement sur Railway + MongoDB

Guide complet pour déployer ScraperbilletV1 sur Railway avec MongoDB Atlas.

## 📋 Prérequis

- [Railway Account](https://railway.app) (gratuit)
- [MongoDB Atlas Account](https://www.mongodb.com/cloud/atlas) (gratuit)
- Git et le repo GitHub configuré

## 🏗️ Étape 1: Créer une base de données MongoDB

### 1.1 Créer un cluster sur MongoDB Atlas

1. Va sur https://www.mongodb.com/cloud/atlas
2. Clique **"Create a Free Account"**
3. Complète le formulaire et confirme l'email
4. Va sur **"Projects"** → **"Create New Project"** → **"Build a Database"**
5. Choisis **"Shared"** (gratuit)
6. Sélectionne une région proche (exemple: **Ireland** pour l'Europe)
7. Clique **"Create Cluster"** et attends ~3-5 minutes

### 1.2 Obtenir la connection string

1. Une fois le cluster créé, clique **"Connect"**
2. Choisis **"Drivers"** → **"Python"** → **"3.12 or later"**
3. Copie la **connection string** (URI)
4. Remplace `<password>` par ton mot de passe
5. Remplace `myFirstDatabase` par `scraperbillet`

**Exemple:**
```
mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/scraperbillet?retryWrites=true&w=majority
```

### 1.3 Ajouter une IP autorisée (important!)

1. Clique sur **"Network Access"** dans MongoDB Atlas
2. Clique **"Add IP Address"**
3. Sélectionne **"Allow Access from Anywhere"** (⚠️ ou spécifie l'IP de Railway)
4. Confirme

## 🚀 Étape 2: Déployer sur Railway

### 2.1 Connecter Railway à GitHub

1. Va sur https://railway.app
2. **Login/Sign Up** avec GitHub
3. Autorise Railway à accéder à tes repos

### 2.2 Créer un nouveau projet

1. Clique **"New Project"**
2. Sélectionne **"Deploy from GitHub repo"**
3. Choisis **"lolbloc99/ScraperbilletV1"**
4. Railway va créer automatiquement le service

### 2.3 Configurer les variables d'environnement

1. Dans le dashboard Railway, va dans ton projet **"ScraperbilletV1"**
2. Clique sur **"Variables"** (ou l'onglet "Settings")
3. Ajoute ces variables:

```
MONGODB_URI=mongodb+srv://username:password@cluster0.xxxxx.mongodb.net/scraperbillet?retryWrites=true&w=majority
PORT=5000
ENVIRONMENT=production
TELEGRAM_BOT_TOKEN=ton_token_telegram (optionnel pour la suite)
TELEGRAM_CHAT_ID=ton_chat_id (optionnel)
```

**Où copier MONGODB_URI:**
- De MongoDB Atlas (voir Étape 1.2)
- Remplace `<password>` par ton vrai mot de passe

### 2.4 Activer les ports

1. Dans Railway, va dans ton service
2. Clique sur **"Networking"**
3. **Port 5000** doit être exposé (Railway fait ça automatiquement)
4. Copie l'URL publique (exemple: `https://yourdomain-prod.up.railway.app`)

## ✅ Étape 3: Vérifier le déploiement

### Vérifier les logs

```bash
# Dans Railway dashboard
1. Clique sur ton projet
2. Va dans l'onglet "Logs"
3. Vérifie que le service a démarré sans erreur
```

Logs attendus:
```
✅ Connecté à MongoDB
⏰ Scraping planifié pour 12:00 chaque jour
✅ Scheduler démarré
🚀 API Flask démarrée sur port 5000
```

### Tester les endpoints

```bash
# Health check (vérifie que le service est actif)
curl https://yourdomain-prod.up.railway.app/health

# Obtenir les statistiques
curl https://yourdomain-prod.up.railway.app/stats

# Récupérer les événements du jour
curl https://yourdomain-prod.up.railway.app/events

# Déclencher un scraping manuel
curl -X POST https://yourdomain-prod.up.railway.app/run
```

### Réponse attendue pour /health

```json
{
  "status": "ok",
  "last_run": "2026-03-15T12:00:00",
  "last_result": {
    "success": true,
    "total_events": 45,
    "new_events": 12
  }
}
```

## 📊 Structure MongoDB

Les données sont stockées dans deux collections:

### Collection `events`
```json
{
  "_id": "a3f8d9c2b1e4f6a7c9d2e1f4",
  "title": "Coldplay at O2 Arena",
  "date": "20 May 2026",
  "market": "UK",
  "platform": "Songkick",
  "url": "https://...",
  "sold_out": true,
  "scraped_at": "2026-03-15T12:00:00",
  "created_at": "2026-03-15T12:00:00"
}
```

### Collection `metadata`
```json
{
  "_id": "last_update",
  "timestamp": "2026-03-15T12:00:00",
  "total_scraped": 45,
  "new_events": 12
}
```

## 🔄 Fonctionnement automatique

- **Démarrage**: Le scraper lance automatiquement au démarrage du conteneur
- **Scraping quotidien**: À 12:00 UTC chaque jour (configurable dans `config.json`)
- **API active 24/7**: Disponible pour des requêtes manuelles

## 📝 Configuration avancée

### Changer l'heure de scraping

Édite `config.json`:
```json
{
  "notification_time": "14:30"  // 14h30 UTC
}
```

Puis push sur GitHub (Railway redéploiera automatiquement).

### Scaler Railway

1. Dans le dashboard, clique sur ton service
2. Va dans **"Deployments"**
3. Configure le nombre de réplicas (pour plus de puissance)

## 🆘 Troubleshooting

### "MongoDB connection failed"
- Vérifie l'URI dans les variables d'environnement
- Vérifie que l'IP est autorisée dans MongoDB Atlas ("Network Access")
- Teste la connexion: `mongo "mongodb+srv://..." --username admin`

### "Port 5000 already in use"
- Railway assigne un port automatiquement, ne force pas le port manuellement

### "Scraping ne se lance pas"
- Vérifie les logs dans Railway Dashboard
- Vérifie que `config.json` est dans le repo

### Chrome/Chromedriver error
- Railway a Chrome et ChromeDriver installés dans le Dockerfile
- Si ça échoue, vérifiez les logs

## 🎯 Prochaines étapes

1. **Intégrer Telegram** (pour les alertes quotidiennes)
2. **Ajouter une API complète** (pour consulter les résultats)
3. **Créer un dashboard** (Web UI pour visualiser les events)

## 📈 Monitoring

### Via Railway Dashboard
- Utilisation CPU/Mémoire
- Logs en temps réel
- Historique des déploiements

### Via MongoDB Atlas
- Taille de la base de données
- Nombre de documents
- Connexions actives

## 💰 Coûts (Gratuit!)

- **Railway**: 5$/month de crédit gratuit (suffit pour ce projet)
- **MongoDB Atlas**: Tier gratuit illimité (512 MB de données)
- **Total**: 0$ si utilisé de manière raisonnable

---

**C'est bon!** Le scraper tourne maintenant 24/7 sur Railway! 🎉

Prochaine étape: **Intégration Telegram** pour recevoir les alertes! 🤖
