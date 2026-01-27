FROM python:3.12-slim

# Installer Tesseract et dépendances système
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-fra \
    && rm -rf /var/lib/apt/lists/*

# Créer le répertoire de travail
WORKDIR /app

# Copier les requirements et installer les dépendances Python
COPY requirements_web.txt .
RUN pip install --no-cache-dir -r requirements_web.txt

# Copier le reste de l'application
COPY . .

# Créer les dossiers nécessaires
RUN mkdir -p uploads outputs signatures

# Exposer le port
EXPOSE 5000

# Variables d'environnement
ENV FLASK_APP=app.py
ENV PYTHONUNBUFFERED=1

# Commande de démarrage
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "--timeout", "120", "app:app"]
