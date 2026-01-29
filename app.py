"""
Application Web pour Signature Automatique de PDF - VERSION SIMPLE
"""

from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from werkzeug.utils import secure_filename
import os
import zipfile
from datetime import datetime
import fitz  # PyMuPDF
from PIL import Image
import io
from pathlib import Path

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
SIGNATURE_FOLDER = 'signatures'
ALLOWED_EXTENSIONS = {'pdf'}
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100 MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OUTPUT_FOLDER'] = OUTPUT_FOLDER
app.config['SIGNATURE_FOLDER'] = SIGNATURE_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Créer les dossiers nécessaires
for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER, SIGNATURE_FOLDER]:
    os.makedirs(folder, exist_ok=True)

# Signature par défaut
DEFAULT_SIGNATURE = os.path.join(SIGNATURE_FOLDER, 'signature_charles.png')


class PDFSigner:
    """Classe pour signer des PDF"""
    
    def __init__(self, signature_path, date_format="%d/%m/%Y"):
        self.signature_path = signature_path
        self.date_format = date_format
        self.current_date = datetime.now().strftime(date_format)
    
    def _find_signature_zone(self, page):
        """Trouve la zone de signature - SEULEMENT dans le cadre responsable"""
        text_instances = page.get_text("dict")
        
        # Chercher SEULEMENT "responsable de la formation" ou "responsable des stages"
        # PAS "cadre administration" (ce cadre est vide)
        responsable_y = None
        target_keywords = [
            ("responsable", "formation"),
            ("responsable", "stage")
        ]
        
        for block in text_instances.get("blocks", []):
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    line_text = ""
                    line_y = None
                    
                    for span in line.get("spans", []):
                        text = span.get("text", "").lower()
                        line_text += text + " "
                        if line_y is None:
                            bbox = span.get("bbox", [])
                            line_y = bbox[1]
                    
                    for keyword1, keyword2 in target_keywords:
                        if keyword1 in line_text and keyword2 in line_text:
                            responsable_y = line_y
                            break
                    
                    if responsable_y:
                        break
        
        if responsable_y:
            signature_candidates = []
            
            for block in text_instances.get("blocks", []):
                if block.get("type") == 0:
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            text = span.get("text", "").lower()
                            bbox = span.get("bbox", [])
                            
                            # Chercher "signature" APRÈS le responsable ET à droite (x > 250)
                            if bbox[1] > responsable_y and "signature" in text and bbox[0] > 250:
                                x = bbox[2] + 10
                                y = bbox[1]
                                signature_candidates.append((x, y, bbox[2]))
            
            if signature_candidates:
                signature_candidates.sort(key=lambda s: s[2], reverse=True)
                return (signature_candidates[0][0], signature_candidates[0][1])
        
        return None
    
    def _find_date_zone(self, page):
        """Trouve la zone de date - SEULEMENT dans le cadre responsable"""
        text_instances = page.get_text("dict")
        
        # Chercher SEULEMENT "responsable"
        responsable_y = None
        target_keywords = [
            ("responsable", "formation"),
            ("responsable", "stage")
        ]
        
        for block in text_instances.get("blocks", []):
            if block.get("type") == 0:
                for line in block.get("lines", []):
                    line_text = ""
                    line_y = None
                    
                    for span in line.get("spans", []):
                        text = span.get("text", "").lower()
                        line_text += text + " "
                        if line_y is None:
                            bbox = span.get("bbox", [])
                            line_y = bbox[1]
                    
                    for keyword1, keyword2 in target_keywords:
                        if keyword1 in line_text and keyword2 in line_text:
                            responsable_y = line_y
                            break
                    
                    if responsable_y:
                        break
        
        if responsable_y:
            for block in text_instances.get("blocks", []):
                if block.get("type") == 0:
                    for line in block.get("lines", []):
                        for span in line.get("spans", []):
                            text = span.get("text", "").lower()
                            bbox = span.get("bbox", [])
                            
                            # Chercher "date" APRÈS le responsable ET à gauche (x < 200)
                            if bbox[1] > responsable_y and "date" in text and bbox[0] < 200:
                                x = bbox[2] + 10
                                y = bbox[1]
                                return (x, y)
        
        return None
    
    def _insert_signature(self, page, position, width=50):
        """Insère la signature"""
        x, y = position
        img = Image.open(self.signature_path)
        aspect_ratio = img.height / img.width
        height = width * aspect_ratio
        
        img_bytes = io.BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        rect = fitz.Rect(x, y - height - 3, x + width, y - 3)
        page.insert_image(rect, stream=img_bytes.getvalue())
    
    def _insert_date(self, page, position, font_size=9):
        """Insère la date"""
        x, y = position
        page.insert_text(
            (x, y),
            self.current_date,
            fontsize=font_size,
            color=(0, 0, 0)
        )
    
    def sign_pdf(self, input_path, output_path, signature_width=50):
        """Signe un PDF - VERSION SIMPLE"""
        try:
            doc = fitz.open(input_path)
            signature_added = False
            date_added = False
            
            # Parcourir les pages de la fin vers le début
            for page_num in range(len(doc) - 1, -1, -1):
                page = doc[page_num]
                
                # Chercher et ajouter la signature
                if not signature_added:
                    sig_pos = self._find_signature_zone(page)
                    if sig_pos:
                        self._insert_signature(page, sig_pos, signature_width)
                        signature_added = True
                
                # Chercher et ajouter la date
                if not date_added:
                    date_pos = self._find_date_zone(page)
                    if date_pos:
                        self._insert_date(page, date_pos)
                        date_added = True
                
                # Si on a tout trouvé, pas besoin de continuer
                if signature_added and date_added:
                    break
            
            # Sauvegarder le PDF
            doc.save(output_path)
            doc.close()
            
            return {
                'success': True,
                'signature_found': signature_added,
                'date_found': date_added
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}


def allowed_file(filename):
    """Vérifie si le fichier est autorisé"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def clean_old_files():
    """Nettoie les vieux fichiers"""
    for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
        for file in Path(folder).glob('*'):
            if file.is_file():
                if (datetime.now().timestamp() - file.stat().st_mtime) > 3600:
                    file.unlink()


@app.route('/')
def index():
    """Page d'accueil"""
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_files():
    """Upload et signature des PDF"""
    
    if 'files[]' not in request.files:
        return jsonify({'error': 'Aucun fichier fourni'}), 400
    
    files = request.files.getlist('files[]')
    
    if not files or files[0].filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    clean_old_files()
    
    if not os.path.exists(DEFAULT_SIGNATURE):
        return jsonify({'error': 'Signature non trouvée'}), 500
    
    signer = PDFSigner(DEFAULT_SIGNATURE)
    
    results = []
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{timestamp}_{filename}"
            
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(input_path)
            
            output_filename = f"signed_{filename}"
            output_path = os.path.join(app.config['OUTPUT_FOLDER'], f"{timestamp}_{output_filename}")
            
            result = signer.sign_pdf(input_path, output_path)
            
            if result['success']:
                results.append({
                    'filename': filename,
                    'output_filename': output_filename,
                    'output_path': f"{timestamp}_{output_filename}",
                    'status': 'success',
                    'signature_found': result['signature_found'],
                    'date_found': result['date_found']
                })
            else:
                results.append({
                    'filename': filename,
                    'status': 'error',
                    'error': result.get('error', 'Erreur inconnue')
                })
            
            os.remove(input_path)
        else:
            results.append({
                'filename': file.filename,
                'status': 'error',
                'error': 'Type de fichier non autorisé'
            })
    
    return jsonify({
        'results': results,
        'total': len(files),
        'success': sum(1 for r in results if r['status'] == 'success'),
        'date': signer.current_date
    })


@app.route('/download/<filename>')
def download_file(filename):
    """Télécharger un fichier signé"""
    try:
        return send_from_directory(
            app.config['OUTPUT_FOLDER'],
            filename,
            as_attachment=True,
            download_name=filename.split('_', 2)[-1]
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 404


@app.route('/download-all')
def download_all():
    """Télécharger tous les PDF signés dans un ZIP"""
    try:
        memory_file = io.BytesIO()
        
        with zipfile.ZipFile(memory_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file in Path(app.config['OUTPUT_FOLDER']).glob('*.pdf'):
                clean_name = '_'.join(file.name.split('_')[2:])
                zipf.write(file, clean_name)
        
        memory_file.seek(0)
        
        return send_file(
            memory_file,
            mimetype='application/zip',
            as_attachment=True,
            download_name=f'pdf_signes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.zip'
        )
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/clear')
def clear_files():
    """Nettoyer les fichiers temporaires"""
    try:
        for folder in [UPLOAD_FOLDER, OUTPUT_FOLDER]:
            for file in Path(folder).glob('*'):
                if file.is_file():
                    file.unlink()
        return jsonify({'success': True, 'message': 'Fichiers nettoyés'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
