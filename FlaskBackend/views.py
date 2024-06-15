import os
from flask import Blueprint, render_template, request, redirect, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
from FlaskBackend.models import Music
from flask_login import login_required, current_user
from FlaskBackend import db

# Stvaranje Blueprinta za povezivanje rutiranja
views = Blueprint('views', __name__)

# Configuration for file upload
UPLOAD_FOLDER = os.path.join(os.getcwd(), 'music_upload')
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'ogg'}  # Allowed file extensions for audio files

# Check if the uploaded file has an allowed extension
def allowed_file(filename):
    global extension
    extension = filename.rsplit('.', 1)[1].lower()
    return '.' in filename and extension in ALLOWED_EXTENSIONS

# Function to create a directory if it doesn't exist
def create_directory(directory='music_upload'):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Prikazuje početnu stranicu sa svim pojmovima
@views.route('/', methods=['POST', 'GET'])
def index():
    musics = Music.query.all()
    if request.method == 'POST':
        name = request.form['name']
        genre = request.form['genre']
        creator = request.form['creator']
        
        # Check if the post request has the file part
        if 'audio_file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['audio_file']
        
        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        
        # Check if the file has an allowed extension
        if file and allowed_file(file.filename):
            music = Music(name=name, genre=genre, creator=creator, audio_file='')
            db.session.add(music)
            db.session.commit()

            create_directory()

            # Generate a unique filename based on music id and file extension
            filename = f"{music.id}.{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)
            
            try:
                # Update the Music object with the file path
                music.audio_file = filename
                db.session.commit()
                return redirect('/')
            except:
                flash('Uploading error')
                return redirect(request.url)

    return render_template('index.html', musics=musics)

@views.route('/music_upload/<path:filename>')
def download_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)
