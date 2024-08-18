from flask import Flask, request, jsonify, send_from_directory, render_template
import os
from werkzeug.utils import secure_filename
import gzip
import io

##Added IO Module 


app = Flask(__name__, static_folder='static', template_folder='templates')
app.config['MAX_CONTENT_LENGTH'] = 3000 * 1024 * 1024
MOVIES_FOLDER = 'E:/MoviesDatabase'
#MOVIES_FOLDER = '/Users/inderdeepsingh/Documents/'
THUMBNAILS_FOLDER = './static/thumbnails/'
UPLOAD_FOLDER = 'E:/MoviesDatabase'
#UPLOAD_FOLDER = '/Users/inderdeepsingh/Documents'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Endpoint to get list of movies
@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = os.listdir(MOVIES_FOLDER)
    return jsonify(movies)


@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    start = int(request.form.get('start', 0))
    filename = file.filename

    # Define the path for the file
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    
    # Open the file in append mode
    with open(file_path, 'ab') as f:
        file.seek(0)
        f.write(file.read())
    
    # Respond with a success message
    return jsonify({'message': 'Chunk uploaded successfully'})

@app.route('/uploads/<filename>', methods=['GET'])
def serve_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)


# Endpoint to stream a movie
@app.route('/movies/<movie_name>', methods=['GET'])
def stream_movie(movie_name):
    return send_from_directory(MOVIES_FOLDER, movie_name)

# Endpoint to serve the main HTML file
@app.route('/')
def index():
    return render_template('index.html')

# Endpoint to serve thumbnails
@app.route('/thumbnails/<thumbnail_name>', methods=['GET'])
def get_thumbnail(thumbnail_name):
    return send_from_directory(THUMBNAILS_FOLDER, thumbnail_name)

if __name__ == '__main__':
    app.run()
