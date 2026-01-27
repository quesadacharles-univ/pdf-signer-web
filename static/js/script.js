// Variables globales
let selectedFiles = [];
let resultsData = [];

// Initialisation
document.addEventListener('DOMContentLoaded', function() {
    setupDragAndDrop();
    setupFileInput();
});

// Configuration du drag & drop
function setupDragAndDrop() {
    const uploadZone = document.getElementById('uploadZone');
    
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.add('dragover');
        }, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        uploadZone.addEventListener(eventName, () => {
            uploadZone.classList.remove('dragover');
        }, false);
    });
    
    uploadZone.addEventListener('drop', handleDrop, false);
}

// Gestion du drop
function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;
    handleFiles(files);
}

// Configuration de l'input file
function setupFileInput() {
    const fileInput = document.getElementById('fileInput');
    fileInput.addEventListener('change', function(e) {
        handleFiles(e.target.files);
    });
}

// Traitement des fichiers sélectionnés
function handleFiles(files) {
    const pdfFiles = Array.from(files).filter(file => 
        file.type === 'application/pdf' || file.name.toLowerCase().endsWith('.pdf')
    );
    
    if (pdfFiles.length === 0) {
        alert('⚠️ Veuillez sélectionner uniquement des fichiers PDF');
        return;
    }
    
    selectedFiles = pdfFiles;
    displaySelectedFiles();
    
    // Afficher la liste et masquer la zone d'upload
    document.getElementById('uploadZone').style.display = 'none';
    document.getElementById('fileList').style.display = 'block';
}

// Affichage des fichiers sélectionnés
function displaySelectedFiles() {
    const container = document.getElementById('selectedFiles');
    container.innerHTML = '';
    
    selectedFiles.forEach((file, index) => {
        const fileItem = document.createElement('div');
        fileItem.className = 'file-item';
        
        const fileSize = formatFileSize(file.size);
        
        fileItem.innerHTML = `
            <div class="file-info">
                <span class="file-icon">📄</span>
                <div>
                    <div class="file-name">${file.name}</div>
                    <div class="file-size">${fileSize}</div>
                </div>
            </div>
            <button class="remove-file" onclick="removeFile(${index})" title="Retirer ce fichier">
                ✖
            </button>
        `;
        
        container.appendChild(fileItem);
    });
}

// Formatage de la taille de fichier
function formatFileSize(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Retirer un fichier de la sélection
function removeFile(index) {
    selectedFiles.splice(index, 1);
    
    if (selectedFiles.length === 0) {
        clearSelection();
    } else {
        displaySelectedFiles();
    }
}

// Annuler la sélection
function clearSelection() {
    selectedFiles = [];
    document.getElementById('fileList').style.display = 'none';
    document.getElementById('uploadZone').style.display = 'block';
    document.getElementById('fileInput').value = '';
}

// Signature des documents
async function signDocuments() {
    if (selectedFiles.length === 0) {
        alert('⚠️ Veuillez sélectionner au moins un fichier');
        return;
    }
    
    // Masquer la liste de fichiers et afficher la progression
    document.getElementById('fileList').style.display = 'none';
    document.getElementById('progressSection').style.display = 'block';
    
    // Préparer les données
    const formData = new FormData();
    selectedFiles.forEach(file => {
        formData.append('files[]', file);
    });
    
    try {
        // Mise à jour de la progression
        updateProgress(10, 'Envoi des fichiers...');
        
        // Envoyer la requête
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });
        
        updateProgress(50, 'Signature en cours...');
        
        if (!response.ok) {
            throw new Error('Erreur lors de l\'envoi des fichiers');
        }
        
        const data = await response.json();
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        updateProgress(100, 'Signature terminée !');
        
        // Attendre un peu pour l'animation
        await new Promise(resolve => setTimeout(resolve, 500));
        
        // Afficher les résultats
        displayResults(data);
        
    } catch (error) {
        alert('❌ Erreur : ' + error.message);
        resetApp();
    }
}

// Mise à jour de la barre de progression
function updateProgress(percent, text) {
    document.getElementById('progressFill').style.width = percent + '%';
    document.getElementById('progressText').textContent = text;
}

// Affichage des résultats
function displayResults(data) {
    resultsData = data.results;
    
    // Masquer la progression
    document.getElementById('progressSection').style.display = 'none';
    
    // Afficher les résultats
    const resultsSection = document.getElementById('resultsSection');
    resultsSection.style.display = 'block';
    
    // Informations générales
    const infoHtml = `
        <p style="font-size: 1.1em; margin-bottom: 20px;">
            📅 Date de signature : <strong>${data.date}</strong>
        </p>
        <div class="results-stats">
            <div class="stat-item">
                <div class="stat-value">${data.total}</div>
                <div class="stat-label">Documents traités</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${data.success}</div>
                <div class="stat-label">Signés avec succès</div>
            </div>
            ${data.total - data.success > 0 ? `
            <div class="stat-item">
                <div class="stat-value">${data.total - data.success}</div>
                <div class="stat-label">Erreurs</div>
            </div>
            ` : ''}
        </div>
    `;
    
    document.getElementById('resultsInfo').innerHTML = infoHtml;
    
    // Liste des résultats
    const resultsList = document.getElementById('resultsList');
    resultsList.innerHTML = '';
    
    data.results.forEach(result => {
        const resultItem = document.createElement('div');
        resultItem.className = 'result-item';
        
        let statusText = '';
        let statusClass = '';
        let iconEmoji = '';
        let downloadBtn = '';
        
        if (result.status === 'success') {
            iconEmoji = '✅';
            statusClass = 'success';
            
            const warnings = [];
            if (!result.signature_found) warnings.push('zone signature non détectée');
            if (!result.date_found) warnings.push('zone date non détectée');
            
            if (warnings.length > 0) {
                statusText = `Signé avec avertissement : ${warnings.join(', ')}`;
                statusClass = 'warning';
                iconEmoji = '⚠️';
            } else {
                statusText = 'Signé et daté avec succès';
            }
            
            downloadBtn = `
                <a href="/download/${result.output_path}" 
                   class="btn-download" 
                   download="${result.output_filename}">
                    📥 Télécharger
                </a>
            `;
        } else {
            iconEmoji = '❌';
            statusClass = 'error';
            statusText = `Erreur : ${result.error}`;
        }
        
        resultItem.innerHTML = `
            <div class="result-info">
                <span class="result-icon">${iconEmoji}</span>
                <div class="result-details">
                    <div class="result-name">${result.filename}</div>
                    <div class="result-status ${statusClass}">${statusText}</div>
                </div>
            </div>
            ${downloadBtn}
        `;
        
        resultsList.appendChild(resultItem);
    });
}

// Télécharger tous les fichiers
function downloadAll() {
    window.location.href = '/download-all';
}

// Réinitialiser l'application
function resetApp() {
    // Nettoyer les fichiers sur le serveur
    fetch('/clear')
        .then(() => {
            // Réinitialiser l'interface
            selectedFiles = [];
            resultsData = [];
            
            document.getElementById('fileList').style.display = 'none';
            document.getElementById('progressSection').style.display = 'none';
            document.getElementById('resultsSection').style.display = 'none';
            document.getElementById('uploadZone').style.display = 'block';
            document.getElementById('fileInput').value = '';
            
            // Réinitialiser la progression
            updateProgress(0, 'Préparation...');
        })
        .catch(error => {
            console.error('Erreur lors du nettoyage:', error);
        });
}

// Gestion du beforeunload
window.addEventListener('beforeunload', function(e) {
    if (selectedFiles.length > 0 || resultsData.length > 0) {
        fetch('/clear');
    }
});
