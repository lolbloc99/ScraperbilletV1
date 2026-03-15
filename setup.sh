#!/bin/bash

# Script d'installation du Concert Scraper

echo "🎵 Installation du Concert Scraper..."
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null
then
    echo "❌ Python 3 n'est pas installé. Veuillez installer Python 3.8+"
    exit 1
fi

echo "✓ Python 3 trouvé: $(python3 --version)"

# Créer environnement virtuel
echo ""
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement
source venv/bin/activate

# Installer les dépendances
echo ""
echo "📥 Installation des dépendances..."
pip install --upgrade pip
pip install -r requirements.txt

# Vérifier/installer ChromeDriver
echo ""
echo "🔧 Installation de ChromeDriver..."

# Pour macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    if ! command -v chromedriver &> /dev/null
    then
        brew install chromedriver
    fi
fi

# Pour Linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    if ! command -v chromedriver &> /dev/null
    then
        apt-get update
        apt-get install -y chromium-chromedriver
    fi
fi

echo ""
echo "✅ Installation terminée!"
echo ""
echo "📖 Pour exécuter le scraper:"
echo "   source venv/bin/activate"
echo "   python3 scraper.py"
echo ""
