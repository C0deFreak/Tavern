from flask import Blueprint, send_from_directory, request, jsonify, send_file
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
import os

views = Blueprint('views', __name__)
FRONTEND_APP = 'frontend'
UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)),'..', '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@views.route('/')
def base():
    return send_from_directory(f'{FRONTEND_APP}/dist', 'index.html')

@views.route('/<path:path>')
def home(path):
    return send_from_directory(f'{FRONTEND_APP}/dist', path)


@views.route('/index')
@login_required
def index():
    return send_file('../../uploads/pmp.mp3')

@views.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    if file:
        filename = secure_filename(file.filename)
        extension = os.path.splitext(filename)[1]
        if extension in ['.mp3', '.wav', '.ogg']:
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return jsonify({"success": 'File uploaded'}), 200
    
    return jsonify({"error": "File upload failed"}), 500
    
