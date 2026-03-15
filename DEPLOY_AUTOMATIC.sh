#!/bin/bash

# Script de déploiement complètement automatisé pour Railway
# Gère tout de A à Z

set -e  # Arrête si une commande échoue

echo "🚀 DÉPLOIEMENT AUTOMATISÉ SCRAPERBILLET V1"
echo "=========================================="
echo ""

# Vérifier les prérequis
echo "📋 Vérification des prérequis..."

if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI non trouvé"
    echo "Installation: npm install -g @railway/cli"
    exit 1
fi

if ! command -v git &> /dev/null; then
    echo "❌ Git non trouvé"
    exit 1
fi

echo "✓ Railway CLI trouvé"
echo "✓ Git trouvé"
echo ""

# Vérifier l'authentification
echo "🔐 Vérification de l'authentification Railway..."
RAILWAY_USER=$(railway whoami 2>/dev/null || echo "")

if [ -z "$RAILWAY_USER" ]; then
    echo "❌ Non authentifié sur Railway"
    echo "Exécute: railway login"
    exit 1
fi

echo "✓ Authentifié: $RAILWAY_USER"
echo ""

# Aller dans le répertoire du projet
PROJECT_DIR="$HOME/ScraperbilletV1"
GITHUB_URL="https://github.com/lolbloc99/ScraperbilletV1.git"

echo "📂 Préparation du répertoire..."
if [ -d "$PROJECT_DIR/.git" ]; then
    echo "✓ Git repo trouvé"
    cd "$PROJECT_DIR"
else
    echo "⚠️ Clone du repo GitHub..."
    rm -rf "$PROJECT_DIR"
    git clone "$GITHUB_URL" "$PROJECT_DIR"
    cd "$PROJECT_DIR"
fi

echo ""
echo "🔄 Vérification de la configuration..."

# Vérifier les fichiers nécessaires
REQUIRED_FILES=("Dockerfile" "main.py" "scraper_mongodb.py" "config.json" "requirements.txt")
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Fichier manquant: $file"
        exit 1
    fi
done

echo "✓ Tous les fichiers nécessaires sont présents"
echo ""

# Créer ou se connecter au projet Railway
echo "🚀 Configuration du projet Railway..."
echo ""

# Vérifier si le projet existe déjà
PROJECT_ID=$(cat .railway/config.json 2>/dev/null | grep -o '"projectId":"[^"]*' | cut -d'"' -f4 || echo "")

if [ -z "$PROJECT_ID" ]; then
    echo "📝 Création du projet Railway..."
    # Initialiser le projet (non-interactif)
    railway init --name ScraperbilletV1 << EOF
lolbloc99's Projects
ScraperbilletV1
EOF

    PROJECT_ID=$(cat .railway/config.json 2>/dev/null | grep -o '"projectId":"[^"]*' | cut -d'"' -f4)
    echo "✓ Projet créé: $PROJECT_ID"
else
    echo "✓ Projet existant trouvé: $PROJECT_ID"
fi

echo ""
echo "⬆️  Déploiement de l'application..."
railway up --detach

echo ""
echo "⏳ Attente du déploiement initial (cela peut prendre 2-3 min)..."
sleep 30

echo ""
echo "📦 Ajout de MongoDB..."

# Ajouter MongoDB (via API si possible)
# Pour l'instant, afficher les instructions
echo ""
echo "⚠️  ÉTAPE MANUELLE COURTE:"
echo "========================"
echo ""
echo "Ouvre ce lien dans ton navigateur:"
echo "👉 https://railway.app/project/$PROJECT_ID"
echo ""
echo "Puis:"
echo "1. Clique '+ Add Service'"
echo "2. Cherche 'MongoDB' et clique"
echo "3. Railway va le configurer automatiquement ✓"
echo ""
echo "Une fois fait, reviens ici et appuie sur ENTRÉE..."
read -p ""

echo ""
echo "✅ Vérification de la configuration..."

# Vérifier que MongoDB est ajouté
echo ""
echo "🔍 Services actuels:"
railway status

echo ""
echo "🎉 DÉPLOIEMENT LANCÉ!"
echo ""
echo "📊 URL du projet:"
echo "https://railway.app/project/$PROJECT_ID"
echo ""
echo "⏳ Attendez 3-5 minutes que tout démarre..."
echo ""
echo "Après le déploiement:"
echo "1. Allez dans Railway Dashboard"
echo "2. Cliquez sur votre service 'ScraperbilletV1'"
echo "3. Allez dans 'Deployments' pour voir l'URL publique"
echo "4. Testez: curl https://yourdomain/health"
echo ""
echo "✨ C'est fait!"
