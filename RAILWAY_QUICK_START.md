# ⚡ Déploiement Railroad en 3 clics

**Déploie ScraperbilletV1 sur Railway avec MongoDB en moins de 5 minutes!**

## 🚀 Déploiement instantané

### Option 1: Bouton "Deploy" (Plus simple!)

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/github?repo=lolbloc99/ScraperbilletV1&envs=MONGODB_URI&MONGODB_URIDescription=URI+MongoDB)

Clique le bouton ci-dessus et Railway fera tout automatiquement!

---

### Option 2: Déploiement manuel (2 min)

**Étape 1: Aller sur Railway**
1. Va sur https://railway.app
2. Login avec GitHub

**Étape 2: Créer un nouveau projet**
1. Clique **"New Project"**
2. Sélectionne **"Deploy from GitHub repo"**
3. Choisis **"lolbloc99/ScraperbilletV1"**

**Étape 3: Ajouter MongoDB**
1. Dans le projet, clique **"+ Add Service"**
2. Cherche **"MongoDB"** et clique dessus
3. Railway l'ajoute automatiquement

**Étape 4: Configurer les variables**
1. Clique sur le service **"ScraperbilletV1"** (l'app)
2. Va dans **"Variables"**
3. Ajoute:
   ```
   MONGODB_URI=${{MongoDB.MONGO_URI}}
   PORT=5000
   ENVIRONMENT=production
   ```

**Étape 5: Déployer**
1. Railway redéploiera automatiquement
2. Attends ~2-3 minutes
3. Voilà! C'est live! 🎉

---

## ✅ Vérifier que ça marche

### Obtenir l'URL publique

1. Dans Railway, clique sur ton projet
2. Va dans l'onglet **"Networking"** ou **"Domains"**
3. Copie l'URL (ex: `https://scraperbilletv1-prod.up.railway.app`)

### Tester les endpoints

```bash
# Health check
curl https://yourdomain-prod.up.railway.app/health

# Voir les stats
curl https://yourdomain-prod.up.railway.app/stats

# Récupérer les événements
curl https://yourdomain-prod.up.railway.app/events

# Lancer un scraping manuel
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

---

## 📊 Vérifier dans MongoDB

1. Va dans le service MongoDB sur Railway
2. Clique sur **"Data"** ou **"Database"**
3. Tu peux explorer les collections:
   - `events` - Tous les événements trouvés
   - `metadata` - Info sur les derniers scrapes

---

## 🔄 Fonctionnement automatique

**Après le déploiement:**
- ✅ Scraping lance automatiquement **à 12h UTC** chaque jour
- ✅ Les événements sont sauvegardés dans MongoDB
- ✅ L'API REST est accessible 24/7
- ✅ Healthcheck tous les 30 secondes

---

## 📝 Variables d'environnement

Railway injecte automatiquement:

```
MONGODB_URI=mongodb+srv://...  # Connexion MongoDB
PORT=5000                       # Port Flask
ENVIRONMENT=production          # Mode production
```

---

## 🎯 Logs en temps réel

1. Va sur le projet Railway
2. Clique sur **"Logs"**
3. Regarde le scraping en action!

Logs attendus:
```
✓ Connecté à MongoDB
⏰ Scraping planifié pour 12:00 chaque jour
✅ Scheduler démarré
🚀 API Flask démarrée sur port 5000
```

---

## ⚠️ Troubleshooting

**"MongoDB connection failed"**
- Attends 30 sec que MongoDB démarre
- Vérifie que le service MongoDB est actif dans Railway

**"Port already in use"**
- Railway assigne le port automatiquement
- Vérifie le dashboard pour l'URL correcte

**"Scraping ne se lance pas"**
- Vérifie les logs dans Railway
- Peux trigger manuellement: `curl -X POST https://yourdomain/run`

---

## 🚀 Prochaines étapes

1. **Telegram** - Recevoir les alertes quotidiennes
2. **Dashboard** - Web UI pour visualiser les events
3. **Webhooks** - Notifications en temps réel

---

**C'est bon!** ScraperbilletV1 tourne maintenant sur Railway! 🎉

Dis-moi quand c'est déployé et on passe à **Telegram!** 🤖
