from flask import Flask, render_template, request, redirect, url_for, flash
import os
from werkzeug.utils import secure_filename
import face_recognition_v3 as fr

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure upload folder and allowed extensions
UPLOAD_FOLDER = 'proyect\known_faces'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('templates', exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_unique_filename(name, folder):
    """Generate a unique filename for additional photos of the same person"""
    base_name = name
    counter = 1
    while os.path.exists(os.path.join(folder, f"{name}.jpg")):
        name = f"{base_name}_{counter}"
        counter += 1
    return f"{name}.jpg"

@app.route('/')
def home():
    try:
        # Get list of unique names (without numbers)
        known_faces = set()
        if os.path.exists(UPLOAD_FOLDER):
            for filename in os.listdir(UPLOAD_FOLDER):
                if filename.endswith(('.jpg', '.jpeg', '.png')):
                    # Remove numbers and extension to get base name
                    base_name = ''.join(c for c in filename.split('.')[0] if not c.isdigit())
                    base_name = base_name.rstrip('_')  # Remove trailing underscore if any
                    known_faces.add(base_name)
        return render_template('index.html', known_faces=sorted(known_faces))
    except Exception as e:
        print(f"Error in home route: {str(e)}")
        return "An error occurred. Check the console for details."

@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            flash('No files selected')
            return redirect(url_for('home'))
        
        files = request.files.getlist('file')  # Get multiple files
        name = request.form.get('name', '').strip()
        
        if not files or not name:
            flash('Please select files and enter a name')
            return redirect(url_for('home'))
        
        successful_uploads = 0
        failed_uploads = 0
        
        for file in files:
            if file and allowed_file(file.filename):
                # Generate unique filename for this person's photo
                filename = get_unique_filename(name, app.config['UPLOAD_FOLDER'])
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                
                # Save the file temporarily
                file.save(file_path)
                
                # Verify face can be detected
                image = face_recognition.load_image_file(file_path)
                face_locations = face_recognition.face_locations(image)
                
                if not face_locations:
                    os.remove(file_path)
                    failed_uploads += 1
                else:
                    successful_uploads += 1
        
        if successful_uploads > 0:
            flash(f'Successfully uploaded {successful_uploads} photo(s) for {name}')
        if failed_uploads > 0:
            flash(f'{failed_uploads} photo(s) had no detectable face and were not saved')
        
        return redirect(url_for('home'))
    
    except Exception as e:
        print(f"Error in upload route: {str(e)}")
        flash('An error occurred during upload')
        return redirect(url_for('home'))

@app.route('/start_recognition')
def start_recognition():
    try:
        flash('Camera is loading... Please wait.')
        known_face_encodings, known_face_names = fr.load_known_faces()
        if known_face_encodings:
            fr.start_camera(known_face_encodings, known_face_names)
        else:
            flash('No faces loaded. Please add some faces first.')
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error in recognition route: {str(e)}")
        flash('An error occurred while starting recognition')
        return redirect(url_for('home'))

@app.route('/delete/<name>', methods=['POST'])
def delete_person(name):
    try:
        deleted_files = 0
        # Delete all files associated with this name
        for filename in os.listdir(UPLOAD_FOLDER):
            # Check if the filename starts with the person's name
            base_name = ''.join(c for c in filename.split('.')[0] if not c.isdigit()).rstrip('_')
            if base_name == name:
                file_path = os.path.join(UPLOAD_FOLDER, filename)
                os.remove(file_path)
                deleted_files += 1
        
        if deleted_files > 0:
            flash(f'Successfully deleted {name} and all associated photos')
        else:
            flash(f'No files found for {name}')
            
        return redirect(url_for('home'))
    except Exception as e:
        print(f"Error deleting person: {str(e)}")
        flash('An error occurred while deleting the person')
        return redirect(url_for('home'))

if __name__ == '__main__':
    try:
        print("Starting Flask application...")
        print("Access the application at http://127.0.0.1:5000")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting application: {str(e)}")