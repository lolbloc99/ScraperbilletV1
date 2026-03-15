#!/bin/bash

# Script de déploiement simplifié pour Railway

echo "🚀 Script de déploiement ScraperbilletV1"
echo "========================================"
echo ""

# Vérifier git
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé"
    exit 1
fi

echo "✓ Git trouvé"
echo ""

# Informations de déploiement
echo "📋 Informations de déploiement:"
echo ""
echo "Repo: https://github.com/lolbloc99/ScraperbilletV1"
echo "Platform: Railway (https://railway.app)"
echo "Database: MongoDB (inclus dans Railway)"
echo ""

echo "📝 Instructions de déploiement:"
echo ""
echo "1️⃣  Va sur: https://railway.app"
echo ""
echo "2️⃣  Clique 'New Project' → 'Deploy from GitHub'"
echo ""
echo "3️⃣  Sélectionne: lolbloc99/ScraperbilletV1"
echo ""
echo "4️⃣  Ajoute le service MongoDB:"
echo "    - Clique '+ Add Service'"
echo "    - Cherche 'MongoDB' et clique"
echo ""
echo "5️⃣  Configure les variables d'environnement:"
echo "    - MONGODB_URI=\${{MongoDB.MONGO_URI}}"
echo "    - PORT=5000"
echo "    - ENVIRONMENT=production"
echo ""
echo "6️⃣  Railway redéploiera automatiquement"
echo ""
echo "7️⃣  Attends 2-3 min et c'est live! 🎉"
echo ""

echo "🔗 Guide détaillé:"
echo "   Voir: RAILWAY_QUICK_START.md"
echo ""

echo "Besoin d'aide?"
echo "- Logs: Railway Dashboard → Logs"
echo "- Tests: curl https://yourdomain-prod.up.railway.app/health"
echo ""
