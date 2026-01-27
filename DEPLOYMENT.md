# 🚀 Guide de Déploiement

Ce guide vous explique comment déployer l'application sur différentes plateformes cloud.

## 📦 Déploiement sur Heroku

Heroku est une plateforme simple et gratuite (tier gratuit) pour héberger votre application.

### Étapes :

1. **Créer un compte Heroku** : https://signup.heroku.com/

2. **Installer Heroku CLI** :
   ```bash
   # Mac
   brew tap heroku/brew && brew install heroku
   
   # Ubuntu
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

3. **Se connecter** :
   ```bash
   heroku login
   ```

4. **Créer l'application** :
   ```bash
   heroku create votre-app-pdf-signer
   ```

5. **Ajouter le buildpack pour Tesseract** :
   ```bash
   heroku buildpacks:add --index 1 heroku-community/apt
   heroku buildpacks:add --index 2 heroku/python
   ```

6. **Déployer** :
   ```bash
   git push heroku main
   ```

7. **Ouvrir l'application** :
   ```bash
   heroku open
   ```

### Configuration

Pour ajuster les ressources :
```bash
heroku ps:scale web=1
```

Pour voir les logs :
```bash
heroku logs --tail
```

---

## 🌊 Déploiement sur Render

Render offre un hébergement gratuit avec SSL automatique.

### Étapes :

1. **Créer un compte** : https://render.com/

2. **Nouveau Web Service** :
   - Connectez votre repository GitHub
   - Build Command : `pip install -r requirements_web.txt`
   - Start Command : `gunicorn app:app`

3. **Variables d'environnement** :
   - Ajouter : `PYTHON_VERSION = 3.12.0`

4. **Déployer** : Cliquez sur "Create Web Service"

---

## 🚂 Déploiement sur Railway

Railway est simple et gratuit pour débuter.

### Étapes :

1. **Créer un compte** : https://railway.app/

2. **Nouveau Projet** :
   - "New Project" → "Deploy from GitHub repo"
   - Sélectionnez votre repository

3. **Configuration automatique** : Railway détecte automatiquement Flask

4. **Custom Start Command** (si nécessaire) :
   ```
   gunicorn -w 4 -b 0.0.0.0:$PORT app:app
   ```

---

## ✈️ Déploiement sur Fly.io

Fly.io offre un excellent service avec support Docker.

### Étapes :

1. **Installer Fly CLI** :
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Se connecter** :
   ```bash
   fly auth login
   ```

3. **Initialiser** :
   ```bash
   fly launch
   ```

4. **Déployer** :
   ```bash
   fly deploy
   ```

---

## 🐳 Déploiement avec Docker

### Local

```bash
# Construire l'image
docker build -t pdf-signer .

# Lancer le conteneur
docker run -p 5000:5000 pdf-signer
```

### Docker Compose

```bash
docker-compose up -d
```

### Docker Hub

```bash
# Tag l'image
docker tag pdf-signer votre-username/pdf-signer:latest

# Push
docker push votre-username/pdf-signer:latest
```

---

## ☁️ Déploiement sur AWS

### AWS Elastic Beanstalk

1. **Installer AWS EB CLI** :
   ```bash
   pip install awsebcli
   ```

2. **Initialiser** :
   ```bash
   eb init -p python-3.12 pdf-signer
   ```

3. **Créer environnement** :
   ```bash
   eb create pdf-signer-env
   ```

4. **Déployer** :
   ```bash
   eb deploy
   ```

### AWS ECS (avec Docker)

1. Créer un repository ECR
2. Push l'image Docker
3. Créer un service ECS
4. Configurer le load balancer

---

## 🔵 Déploiement sur Azure

### Azure App Service

1. **Installer Azure CLI** :
   ```bash
   curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
   ```

2. **Se connecter** :
   ```bash
   az login
   ```

3. **Créer le groupe de ressources** :
   ```bash
   az group create --name pdf-signer-rg --location westeurope
   ```

4. **Créer l'App Service** :
   ```bash
   az webapp up --runtime PYTHON:3.12 --sku B1 --name pdf-signer-app
   ```

---

## 🟢 Déploiement sur Google Cloud

### Google App Engine

1. **Créer `app.yaml`** :
   ```yaml
   runtime: python312
   entrypoint: gunicorn -b :$PORT app:app
   
   instance_class: F2
   
   automatic_scaling:
     min_instances: 0
     max_instances: 3
   ```

2. **Déployer** :
   ```bash
   gcloud app deploy
   ```

---

## 🔒 Sécurité en Production

Avant de déployer en production :

1. **Activer HTTPS** (automatique sur la plupart des plateformes)

2. **Ajouter des variables d'environnement** :
   ```python
   # Dans app.py
   import os
   app.config['MAX_CONTENT_LENGTH'] = int(os.getenv('MAX_FILE_SIZE', 50 * 1024 * 1024))
   ```

3. **Rate Limiting** :
   ```bash
   pip install Flask-Limiter
   ```

4. **Authentification** (optionnel) :
   ```bash
   pip install Flask-Login
   ```

5. **Monitoring** : Configurer les logs et alertes

---

## 📊 Monitoring et Logs

### Heroku
```bash
heroku logs --tail
heroku addons:create papertrail
```

### Render / Railway
Logs disponibles dans le dashboard

### Docker
```bash
docker logs -f container_name
```

---

## 🎯 Recommandations

**Pour débuter** : Render ou Railway (gratuit, simple)
**Pour scale** : AWS ou Google Cloud (flexible, puissant)
**Pour Docker** : Fly.io ou AWS ECS (moderne, efficace)

---

## ⚠️ Notes Importantes

- Toutes les plateformes gratuites ont des limitations (temps d'exécution, mémoire, etc.)
- Pensez à sécuriser votre application avant un usage public
- Configurez des sauvegardes automatiques si nécessaire
- Testez toujours en local avant de déployer

---

**Besoin d'aide ?** Consultez la documentation de chaque plateforme ou ouvrez une issue sur GitHub.
