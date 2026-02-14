from flask import Flask, request, jsonify, render_template
from flask_cors import CORS  # Permite que el frontend se comunique con el backend
import os
import uuid

app = Flask(__name__)
CORS(app)  # Activamos el permiso de conexión

# Carpeta donde se guardan los archivos subidos
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '../uploads')
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Listas para manejar los estados de los archivos
pending_files = []
processed_files = {}  # Formato: {nombre_archivo: {'json':..., 'midi':..., 'musicxml':...}}

@app.route('/')
def index():
    return '''
    <h2>Sube tu archivo MP3 - Servidor de Thud</h2>
    <form method="post" action="/upload" enctype="multipart/form-data">
        <input type="file" name="file" accept=".mp3" required>
        <input type="submit" value="Subir">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No se subió ningún archivo', 400
    
    file = request.files['file']
    
    if file.filename == '':
        return 'Archivo vacío', 400
    
    # Crear nombre único para evitar choques entre usuarios
    filename = f"{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    # Guardar archivo en la carpeta uploads
    file.save(filepath)
    
    # Marcar como pendiente para el procesamiento
    pending_files.append(filename)
    
    return f'Archivo subido correctamente: {filename}'

@app.route('/pending', methods=['GET'])
def get_pending_files():
    return jsonify({'pendientes': pending_files})

@app.route('/process/<filename>', methods=['GET'])
def get_file_status(filename):
    if filename in pending_files:
        return jsonify({'archivo': filename, 'estado': 'pendiente'})
    elif filename in processed_files:
        return jsonify({'archivo': filename, 'estado': 'procesado'})
    else:
        return jsonify({'archivo': filename, 'estado': 'no encontrado'})

@app.route('/get_score/<filename>', methods=['GET'])
def get_score(filename):
    if filename in processed_files:
        return jsonify({
            'archivo': filename,
            'json': processed_files[filename]['json'],
            'midi': processed_files[filename]['midi'],
            'musicxml': processed_files[filename]['musicxml']
        })
    else:
        return jsonify({'error': 'Archivo no procesado o no encontrado'}), 404

if __name__ == '__main__':
    app.run(debug=True)