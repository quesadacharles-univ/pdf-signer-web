#!/bin/bash

echo "=========================================="
echo "🚀 DÉMARRAGE RAPIDE - PDF AUTO SIGNER"
echo "=========================================="
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 non installé"
    exit 1
fi

echo "✅ Python détecté: $(python3 --version)"

# Vérifier Tesseract
if ! command -v tesseract &> /dev/null; then
    echo "⚠️  Tesseract OCR non installé"
    echo "   Installation automatique..."
    
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        sudo apt-get update
        sudo apt-get install -y tesseract-ocr tesseract-ocr-fra
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        brew install tesseract tesseract-lang
    else
        echo "❌ Système non supporté pour installation automatique"
        echo "   Installez Tesseract manuellement:"
        echo "   https://github.com/tesseract-ocr/tesseract"
        exit 1
    fi
fi

echo "✅ Tesseract détecté: $(tesseract --version | head -n1)"
echo ""

# Créer un environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement
echo "🔄 Activation de l'environnement..."
source venv/bin/activate 2>/dev/null || . venv/bin/activate 2>/dev/null || venv\Scripts\activate.bat 2>/dev/null

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements_web.txt

echo ""
echo "=========================================="
echo "✅ INSTALLATION TERMINÉE!"
echo "=========================================="
echo ""
echo "🎯 Pour démarrer l'application:"
echo ""
echo "1. Activez l'environnement virtuel:"
echo "   source venv/bin/activate  (Linux/Mac)"
echo "   venv\\Scripts\\activate    (Windows)"
echo ""
echo "2. Lancez l'application:"
echo "   python app.py"
echo ""
echo "3. Ouvrez votre navigateur:"
echo "   http://localhost:5000"
echo ""
echo "=========================================="
echo ""
echo "💡 ASTUCES:"
echo "  - Placez votre signature dans: signatures/signature_charles.png"
echo "  - Pour Docker: docker-compose up"
echo "  - Documentation: README_WEB.md"
echo ""
