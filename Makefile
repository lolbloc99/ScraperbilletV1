.PHONY: install test run view view-new logs clean help

help:
	@echo "🎵 Concert Scraper - Commandes disponibles"
	@echo ""
	@echo "  make install      Installation initiale"
	@echo "  make test         Tester la configuration"
	@echo "  make run          Lancer le scraper"
	@echo "  make view         Afficher tous les événements"
	@echo "  make view-new     Afficher nouveaux événements du jour"
	@echo "  make logs         Afficher les logs"
	@echo "  make clean        Nettoyer les fichiers temporaires"
	@echo ""

install:
	@echo "📦 Installation..."
	bash setup.sh

test:
	@echo "🧪 Lancement des tests..."
	. venv/bin/activate && python3 test_scraper.py

run:
	@echo "🚀 Lancement du scraper..."
	. venv/bin/activate && python3 scraper.py

view:
	@echo "📊 Affichage des événements..."
	. venv/bin/activate && python3 view_events.py

view-new:
	@echo "✨ Nouveaux événements du jour..."
	. venv/bin/activate && python3 view_events.py --new

logs:
	@echo "📋 Derniers logs:"
	@tail -50 scraper.log

clean:
	@echo "🧹 Nettoyage..."
	rm -rf __pycache__
	rm -f *.pyc
	find . -type d -name __pycache__ -delete
	@echo "✓ Nettoyage terminé"

.PHONY: help install test run view view-new logs clean
