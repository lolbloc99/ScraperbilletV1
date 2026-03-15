FROM python:3.11-slim

WORKDIR /app

# Installer uniquement ce qui est nécessaire
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copier requirements
COPY requirements.txt .

# Installer les dépendances Python (sans selenium pour le test)
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Exposer le port
EXPOSE 5000

# Démarrer l'app
CMD ["python3", "main.py"]
