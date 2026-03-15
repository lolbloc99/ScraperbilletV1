FROM python:3.11-slim

WORKDIR /app

# Installer Chromium ET ChromeDriver pour Selenium
RUN apt-get update && apt-get install -y \
    curl \
    chromium \
    chromium-driver \
    fonts-liberation \
    libnss3 \
    libxss1 \
    libappindicator1 \
    libindicator7 \
    && rm -rf /var/lib/apt/lists/*

# Set Chromium binary path pour webdriver-manager
ENV GOOGLE_CHROME_BIN=/usr/bin/chromium
ENV CHROMEDRIVER_BIN=/usr/bin/chromedriver

# Copier requirements
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code
COPY . .

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Exposer le port
EXPOSE 5000

# Build timestamp to force rebuild
RUN echo "Build: 2026-03-15T15:10:00Z"

# Démarrer l'app
CMD ["python3", "main.py"]
