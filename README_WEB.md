# 📝 Application Web de Signature Automatique de PDF

Application web moderne permettant de signer et dater automatiquement des documents PDF en ligne.

## 🌟 Fonctionnalités

- ✅ **Interface drag & drop** intuitive
- ✅ **Traitement par lot** - signez plusieurs PDF en une fois
- ✅ **Détection automatique** des zones signature et date
- ✅ **Date automatique** - insertion de la date du jour
- ✅ **Téléchargement individuel** ou **groupé en ZIP**
- ✅ **Design responsive** - fonctionne sur mobile et desktop
- ✅ **Aucune sauvegarde** - fichiers supprimés après téléchargement

## 🚀 Démonstration

![Screenshot](screenshot.png)

## 📋 Prérequis

- Python 3.8+
- Tesseract OCR

## 🔧 Installation

### 1. Cloner le repository

```bash
git clone https://github.com/votre-username/pdf-auto-signer-web.git
cd pdf-auto-signer-web
```

### 2. Installer Tesseract OCR

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-fra
```

**macOS:**
```bash
brew install tesseract tesseract-lang
```

**Windows:**
Télécharger depuis: https://github.com/UB-Mannheim/tesseract/wiki

### 3. Installer les dépendances Python

```bash
pip install -r requirements_web.txt
```

### 4. Ajouter votre signature

Placez votre image de signature (PNG recommandé) dans le dossier `signatures/` avec le nom `signature_charles.png`.

Ou modifiez la ligne dans `app.py` :
```python
DEFAULT_SIGNATURE = os.path.join(SIGNATURE_FOLDER, 'votre_signature.png')
```

## 🏃 Lancement

### Mode développement

```bash
python app.py
```

L'application sera accessible sur : `http://localhost:5000`

### Mode production (avec Gunicorn)

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 🐳 Déploiement avec Docker

```dockerfile
# Dockerfile inclus dans le projet
docker build -t pdf-signer .
docker run -p 5000:5000 pdf-signer
```

## ☁️ Déploiement sur le cloud

### Heroku

```bash
# Installer Heroku CLI puis :
heroku create votre-app-name
git push heroku main
```

### Render / Railway / Fly.io

1. Connectez votre repository GitHub
2. Définissez la commande de démarrage : `gunicorn app:app`
3. Configurez les variables d'environnement si nécessaire

## 📁 Structure du projet

```
pdf-auto-signer-web/
├── app.py                 # Application Flask principale
├── requirements_web.txt   # Dépendances Python
├── .gitignore            # Fichiers à ignorer
├── README.md             # Documentation
├── Dockerfile            # Configuration Docker (optionnel)
├── templates/
│   └── index.html        # Interface utilisateur
├── static/
│   ├── css/
│   │   └── style.css     # Styles CSS
│   └── js/
│       └── script.js     # Logique JavaScript
├── signatures/
│   └── signature_charles.png  # Votre signature
├── uploads/              # Fichiers uploadés (temporaire)
└── outputs/              # Fichiers signés (temporaire)
```

## 🎨 Personnalisation

### Modifier la signature

Remplacez `signatures/signature_charles.png` par votre propre signature.

### Ajuster la taille de signature

Dans `app.py`, modifiez la fonction `sign_pdf` :

```python
signer.sign_pdf(input_path, output_path, signature_width=80)  # Changez 80
```

### Format de date

Dans `app.py`, classe `PDFSigner` :

```python
def __init__(self, signature_path, date_format="%d/%m/%Y"):  # Modifiez le format
```

Formats disponibles :
- `%d/%m/%Y` → 27/01/2026
- `%Y-%m-%d` → 2026-01-27
- `%d %B %Y` → 27 janvier 2026

### Couleurs et design

Modifiez `static/css/style.css` pour personnaliser les couleurs, polices, etc.

## 🔒 Sécurité

- Les fichiers sont stockés temporairement et supprimés après 1 heure
- Limitation de taille : 50 MB par fichier
- Seuls les fichiers PDF sont acceptés
- Pas de sauvegarde permanente des données

**⚠️ Note de sécurité :** Pour un usage en production publique, ajoutez :
- Authentification utilisateur
- HTTPS obligatoire
- Rate limiting
- Scan antivirus des fichiers uploadés

## 🛠️ Dépannage

### Tesseract non trouvé

```bash
# Vérifier l'installation
tesseract --version

# Sous Windows, ajouter au PATH ou modifier app.py :
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

### Port déjà utilisé

Changez le port dans `app.py` :
```python
app.run(debug=True, host='0.0.0.0', port=8000)  # Changez 5000 en 8000
```

### Erreur d'upload

Vérifiez les permissions des dossiers `uploads/` et `outputs/` :
```bash
chmod 755 uploads outputs
```

## 📊 API Endpoints

- `GET /` - Interface principale
- `POST /upload` - Upload et signature des PDF
- `GET /download/<filename>` - Télécharge un fichier individuel
- `GET /download-all` - Télécharge tous les fichiers en ZIP
- `GET /clear` - Nettoie les fichiers temporaires

## 🤝 Contribution

Les contributions sont les bienvenues ! 

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## 📝 Licence

Ce projet est libre d'utilisation pour usage personnel et professionnel.

## 👤 Auteur

**Charles** - Université Jean Monnet de Saint-Étienne

## 🙏 Remerciements

- PyMuPDF pour la manipulation de PDF
- Flask pour le framework web
- Tesseract pour l'OCR

## 📧 Support

Pour toute question ou problème, ouvrez une issue sur GitHub.

---

**Fait avec ❤️ pour simplifier la signature de documents**
